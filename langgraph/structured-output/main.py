import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from typing import Annotated, TypedDict
from pydantic import BaseModel, Field

load_dotenv()

# Define state
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    quality_score: Annotated[int, None]
    num_words: Annotated[int, None]

# Create the graph
builder = StateGraph(GraphState)

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

class GenerateCode(BaseModel):
    """Extract the generated code and the number of words in the code"""
    code: str = Field(description="Generated software code")
    num_words: int = Field(description="Number of words in the generated code")

class QualityScore(BaseModel):
    """Evaluate code quality and extract quality score along with the comment"""
    quality_score: int = Field(description="Code quality score between 0-1000")
    comment: str = Field(description="Comment on the quality score")

developer_structured_llm = llm.with_structured_output(GenerateCode, method="json_mode")

reviewer_structured_llm = llm.with_structured_output(QualityScore, method="json_mode")

# Set initial state
def init(state):
    print('------ Init ------')
    print("State: ", state)
    return {"messages": [], "quality_score": 0, "num_words": 0}

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
    
    return {"messages": [message.code], "num_words": message.num_words}

# Create reviewer node
def reviewer(state):
    print('------ Reviewer START ------')
    
    # Define the system prompt
    system_prompt = "You are a high-standards code reviewer. Review the code provided by Developer and assign a quality Score between 0-1000. Assess the structure, code quality and documentation of the code. Inspect if accepted design patterns are used. Respond in JSON with `quality_score` and `comment` keys."

    human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
    ai_messages = [msg for msg in state["messages"] if isinstance(msg, AIMessage)]
    system_message = [SystemMessage(content=system_prompt)]
    messages = system_message + human_messages + ai_messages

    
    # Invoke the structured LLM
    message = reviewer_structured_llm.invoke(messages)
    quality_score = message.quality_score
    comment = message.comment
    print("Quality Score: ", quality_score)
    print("Comment: ", comment)
    print('------ Reviewer END ------\n\n')
    return {"messages": [comment], "quality_score": quality_score}

# Create summary node
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
builder.add_edge("reviewer", "summary")
builder.add_edge('summary', END)

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