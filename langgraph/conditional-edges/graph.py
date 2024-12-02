import os
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

max_tokens = 2000
num_iterations = 5
quality_threshold = 950

class GenerateCode(BaseModel):
    code: str = Field(description="Generated software code")
    num_words: int = Field(description="Number of words in the generated code")

class QualityScore(BaseModel):
    score: int = Field(description="Quality score between 0-1000")
    comment: str = Field(description="Comment on the quality score")

# Define state
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    quality: Annotated[int, None]
    iterations: Annotated[int, None]

# Create the graph
builder = StateGraph(GraphState)

# Create the LLM
llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("AZURE_OPENAI_API_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    temperature=0,
    max_tokens=max_tokens,
    timeout=None,
    max_retries=2,
)

developer_structured_llm = llm.with_structured_output(GenerateCode, method="json_mode")
reviewer_structured_llm = llm.with_structured_output(QualityScore, method="json_mode")

# Set initial state
def init(state):
    print('------ Init ------')
    print("State: ", state)
    return {"messages": [], "iterations": 0}

# Create developer node
def developer(state):
    print('------ Developer START ------')
    system_prompt = "You are a software developer. Write code for the software per the user instructions. Follow best practices and include comments. Respond in JSON with `code` key containing the generated code and `num_words` containing the count of words in the generated code."
    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    ai_messages = [msg for msg in state["messages"] if isinstance(msg, AIMessage)]
    system_message = [SystemMessage(content=system_prompt)]
    messages = system_message + human_messages + ai_messages

    # Invoke the structured LLM
    message = developer_structured_llm.invoke(messages)
    print("Code: ", message.code)
    print('------ Developer END ------\n\n')
    
    return {"messages": [message.code], "iterations": state['iterations']+1}

# Create reviewer node
def reviewer(state):
    print('------ Reviewer START ------')
    
    # Define the system prompt
    system_prompt = "You are a high-standards code reviewer. Review the code provided by Developer and assign a quality score between 0-1000. Assess the structure, code quality and documentation of the code. Inspect if accepted design patterns are used. Respond in JSON with `score` and `comment` keys."
    
    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    ai_messages = [msg for msg in state["messages"] if isinstance(msg, AIMessage)]
    system_message = [SystemMessage(content=system_prompt)]
    messages = system_message + human_messages + ai_messages
    
    # Invoke the structured LLM
    message = reviewer_structured_llm.invoke(messages)
    score = message.score
    comment = message.comment
    print("Quality Score: ", score)
    print("Comment: ", comment)
    print('------ Reviewer END ------\n\n')

    if score < quality_threshold:
        comment = "The code quality is not up to the mark. Please rewrite the code according to my review comments. " + comment
    return {"messages": [comment], "quality": score}

def summary(state):
    print('------ Summary START ------')
    print("Summary State: ", state)
    print('------ Summary END ------\n\n')
    return state

# Add the node to the graph
builder.add_node("init", init)
builder.add_node("developer", developer)
builder.add_node("reviewer", reviewer)
builder.add_node("summary", summary)

# Set entry point and edge
builder.add_edge(START, "init")
builder.add_edge("init", "developer")
builder.add_edge("developer", "reviewer")
builder.add_edge('summary', END)

# Method for a conditional edge, based on the quality score
def quality_gate_condition(state)->Literal["developer", "summary"]:
    # If more than num_iterations iterations, go to summary
    if state["iterations"] >= num_iterations:
        return "summary"
    
    # If quality is less than quality_threshold, go back to developer for a rewrite
    if state["quality"] < quality_threshold:
        return "developer"
    else:
        return "summary"

# Add conditional edge
builder.add_conditional_edges("reviewer", quality_gate_condition)

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

        graph.invoke({"messages": [HumanMessage(content=user_input)]})

# Run the main loop
if __name__ == "__main__":
    main_loop()
