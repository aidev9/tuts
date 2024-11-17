import os
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
load_dotenv()

# Define state
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]

# Create the graph
builder = StateGraph(GraphState)

# Create the LLM
llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("AZURE_OPENAI_API_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    temperature=0,
    max_tokens=1000,
    timeout=None,
    max_retries=2,
)

def create_node(state, system_prompt):
    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    ai_messages = [msg for msg in state["messages"] if isinstance(msg, AIMessage)]
    system_message = [SystemMessage(content=system_prompt)]
    messages = system_message + human_messages + ai_messages
    message = llm.invoke(messages)
    return {"messages": [message]}

analyst = lambda state: create_node(state, "You are a software requirements analyst. Review the provided instructions and generate software development requirements that a developer can understand and create code from. Be precise and clear in your requirements.")

architect = lambda state: create_node(state, "You are an Software Architect who can design scalable systems that work in cloud environments. Review the software requirements provided and create an architecture document that will be used by developers, testers and designers to implement the system. Provide the architecture only.")

developer = lambda state: create_node(state, "You are an Full Stack Developer and can code in any language. Review the provided instructions and write the code. Return the coding artifacts only.")

reviewer = lambda state: create_node(state, "You are an experienced developer and code reviewer. You know the best design patterns for web applications that run on the cloud and can do code reviews in any language. Review the provided code and suggest improvements. Only focus on the provided code and suggest actionable items.")

tester = lambda state: create_node(state, "You are a test automation expert who can create test scripts in any language. Review the provided user instructions, software requirements and write test code to ensure good quality of the software.")

diagram_designer = lambda state: create_node(state, "You are a Software Designer and can draw diagrams explaining any code. Review the provided code and create a Mermaid diagram explaining the code.")

summary_writer = lambda state: create_node(state, "You are an expert in creating technical documentation and can summarize complex documents into human-readable documents. Review the provided messages and create a meaningful summary. Retain all the source code generated and include it in the summary.")


# Add nodes to the graph
builder.add_node("analyst", analyst)
builder.add_node("architect", architect)
builder.add_node("developer", developer)
builder.add_node("reviewer", reviewer)
builder.add_node("tester", tester)
builder.add_node("diagram_designer", diagram_designer)
builder.add_node("summary_writer", summary_writer)


# Set entry point and edges
builder.add_edge(START, "analyst")
builder.add_edge("analyst", "architect")
builder.add_edge("architect", "developer")
builder.add_edge("developer", "reviewer")
builder.add_edge("reviewer", "tester")
builder.add_edge("tester", "diagram_designer")
builder.add_edge("diagram_designer", "summary_writer")
builder.add_edge("summary_writer", END)

# Compile and run the builder
graph = builder.compile()

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

        response = graph.invoke({"messages": [HumanMessage(content=user_input)]})
        print("Analyst: ", response["messages"][-7].content)
        print("Architect: ", response["messages"][-6].content)
        print("Developer: ", response["messages"][-5].content)
        print("Reviewer: ", response["messages"][-4].content)
        print("Tester: ", response["messages"][-3].content)
        print("Diagram Designer: ", response["messages"][-2].content)
        print("Summary Writer: ", response["messages"][-1].content)

# Run the main loop
if __name__ == "__main__":
    main_loop()