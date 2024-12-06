import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict, Literal
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_experimental.utilities import PythonREPL
import matplotlib
from langchain_community.tools.tavily_search import TavilySearchResults
import requests

load_dotenv()
max_tokens = 2000

# Create the LLM
llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("AZURE_OPENAI_API_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    temperature=0,
    max_tokens=max_tokens,
    timeout=None,
    max_retries=2,
)

# Define the tools
@tool
def llm_tool(
    query: Annotated[str, "The query to search for."]
):
    """A tool to call an LLM model to search for a query"""
    try:
        result = llm.invoke(query)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    return result.content

# File management tools
file_tools = FileManagementToolkit(
    root_dir=str("./data"),
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()
read_tool, write_tool, list_tool = file_tools

repl = PythonREPL()
@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute user instructions such as generate CSV or charts."],
):
    """Use this to execute python code and do math. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user.
    If you need to save a plot, you should save it to the ./data folder. Asumme the most default values for charts and plots. If the user has not indicated a prefence, make an assumtiption and create the plot. Do not use a sandboxed environment. Write the files to the ./data folder, residing in the current folder.

    Clean the data provided before plotting a chart. If arrays are of unequal length, substitute missing data points with 0 or the average of the array.

    Example:
        Do not save the plot to (sandbox:/data/plot.png) but to (./data/plot.png)

    Example:
    ``` from matplotlib import pyplot as plt
        plt.savefig('./data/foo.png')
    ```
    """
    try:
        matplotlib.use('agg')
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return result_str

tavily_tool = TavilySearchResults(max_results=5)

def get_natural_gas():
    response = requests.get(
        "https://www.alphavantage.co/query/",
        params={
            "function": "NATURAL_GAS",
            "apikey": os.getenv("ALPHAVANTAGE_API_KEY"),
        },
    )
    response.raise_for_status()
    data = response.json()

    if "Error Message" in data:
        raise ValueError(f"API Error: {data['Error Message']}")

    return data

@tool
def alpha_vantage_tool():
    """A tool to get Natural Gas prices from AlphaVantage API"""
    try:
        result = get_natural_gas()
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    return result

def get_gdp_data(country_code: str):
    response = requests.get(
        "https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH",
    )
    response.raise_for_status()
    data = response.json()

    if "Error Message" in data:
        raise ValueError(f"API Error: {data['Error Message']}")

    return data["values"]["NGDP_RPCH"][country_code]

@tool
def gdp_tool(country_code: str):
    """A tool to get the GDP data for a given country code"""
    try:
        result = get_gdp_data(country_code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    return result

# The agent state is the input to each node in the graph
class AgentState(MessagesState):
    # The 'next' field indicates where to route to next
    next: str

# Member agent names
members = ["llm", "file_writer", "coder", "researcher", "alpha_vantage", "gdp_researcher"]

# Our team supervisor is an LLM node. It just picks the next agent to process and decides when the work is completed
options = members + ["FINISH"]

system_prompt = (
    f"""You are a supervisor tasked with managing a conversation between the following workers: {members}. Given the following user request, respond with the worker to act next. Each worker will perform a task and respond with their results and status. When finished, respond with FINISH.Always start with the question and see if you can answer it without any tools. Then only call the llm tool and then call research tool, only when the LLM tool results are inadequate. If no tools are needed, route to llm agent. For calculations, visualizations, plots, charts, CSV file generation, use the coder worker. For example, if the user asks for a bar chart, ask the researcher to gather the data and then the coder to create and save the plot. For GDP research, use the gdp_tool by passing the country code. For research, use the researcher worker. If you're asked to get historical data for Natural Gas prices, do not use Research tool, go straight to alpha_vantage_tool and ask coder to use the data provided. For file management, use the file_writer worker only after the tasks of the researcher and the coder are done and if the user requires any file operations. FINISH only when all tasks are done. Do not end the conversation until all tasks are complete. Do not end the conversation until the file is written. All files should be written in ./data residing in the current folder."""
)

class SupervisorState(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal[*options]

# Nodes
def supervisor_node(state: AgentState) -> AgentState:
    print("----------------- SUPERVISOR NODE START -----------------\n")
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    response = llm.with_structured_output(SupervisorState).invoke(messages)
    next_ = response["next"]
    if next_ == "FINISH":
        next_ = END

    print(f"Routing to {next_}")
    print("----------------- SUPERVISOR NODE END -----------------\n")
    return {"next": next_}

llm_agent = create_react_agent(
    llm, tools=[llm_tool], state_modifier="You are a highly-trained research analyst and can provide the user with the information they need. You are tasked with finding the answer to the user's question without using any tools. Answer the user's question to the best of your ability."
)

file_agent = create_react_agent(llm, tools=[write_tool])
def file_node(state: AgentState) -> AgentState:
    result = file_agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name="file_writer")]
    }

def llm_node(state: AgentState) -> AgentState:
    result = llm_agent.invoke(state)
    return {
        "messages": [
            HumanMessage(content=result["messages"][-1].content, name="llm_node")
        ]
    }

code_agent = create_react_agent(llm, tools=[python_repl_tool])
def code_node(state: AgentState) -> AgentState:
    result = code_agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name="coder")]
    }

research_agent = create_react_agent(
    llm, tools=[tavily_tool], state_modifier="You are a highly-trained researcher. DO NOT do any math. You are tasked with finding the answer to the user's question. You have access to the following tools: Tavily Search. Use them wisely."
)
def research_node(state: AgentState) -> AgentState:
    result = research_agent.invoke(state)

    return {
        "messages": [
            HumanMessage(content=result["messages"][-1].content, name="researcher")
        ]
    }

alpha_vantage_agent = create_react_agent(llm, tools=[alpha_vantage_tool])
def alpha_vantage_node(state: AgentState) -> AgentState:
    result = alpha_vantage_agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name="alpha_vantage")]
    }

gdp_agent = create_react_agent(llm, tools=[gdp_tool])
def gdp_node(state: AgentState) -> AgentState:
    result = gdp_agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name="gdp_researcher")]
    }

builder = StateGraph(AgentState)
builder.add_node("supervisor", supervisor_node)
builder.add_edge(START, "supervisor")
builder.add_node("llm", llm_node)
builder.add_node("file_writer", file_node)
builder.add_node("coder", code_node)
builder.add_node("researcher", research_node)
builder.add_node("alpha_vantage", alpha_vantage_node)
builder.add_node("gdp_researcher", gdp_node)

# Set the configuration needed for the state
config = {"configurable": {"thread_id": "1"}}
memory = MemorySaver()

for member in members:
    # We want our workers to ALWAYS "report back" to the supervisor when done
    builder.add_edge(member, "supervisor")

# The supervisor populates the "next" field in the graph state which routes to a node or finishes
builder.add_conditional_edges("supervisor", lambda state: state["next"])

# Compile the graph
graph = builder.compile(checkpointer=memory)

# Draw the graph
try:
    graph.get_graph(xray=True).draw_mermaid_png(output_file_path="graph.png")
except Exception:
    pass

# Create a main loop
def main_loop():
    # Run the chatbot
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        for s in graph.stream(
            {
                "messages": [
                    (
                        "user", user_input
                    )
                ]
            },
            config=config,
        ):
            print(s)
            print("----")

# Run the main loop
if __name__ == "__main__":
    main_loop()