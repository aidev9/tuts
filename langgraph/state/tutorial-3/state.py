'''
    In this step, we will create a StateGraph that will use TypedDict to define the state of the graph. The graph will hold a list of the Fibonacci numbers.

    We will persist the state of the graph using SQLite as long-term memory. We will use the SqliteSaver class from the langgraph.checkpoint.sqlite module to save the state of the graph to a SQLite database. Saving conversational threads to a database allows us to resume the conversation at a later time.
    
    We will also update the initial state of the graph to include the first three Fibonacci numbers.

    We will draw a visualization of the graph using the draw_mermaid_png method. This method generates a PNG image of the graph using the Mermaid library.
    
    Finally, we will run the chatbot and print the next Fibonacci number in the sequence.
'''

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

# Calculate next Fibonacci number
def fibonacci(n: int) -> int:
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    
# Define reducer
def fibonacci_reducer(current: list[int], update: int | None) -> list[int]:
    if current is None:
        current = []
    if update is None:
        return current
    return sorted(list(set(current + update)))    

# Define state
class GraphState(TypedDict):
    fibonacci: Annotated[list[int], fibonacci_reducer]

# Create the graph
builder = StateGraph(GraphState)

# Create developer node
def developer(state):
    return state  # Return the modified state

# Add the node to the graph
builder.add_node("developer", developer)

# Set entry point and edge
builder.add_edge(START, "developer")
builder.add_edge('developer', END)

# Configuration and memory
config = {"configurable": {"thread_id": 2}}

# Create a connection to the SQLite database
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

# Compile and run the builder
graph = builder.compile(checkpointer=memory)

# Provide the initial state
initial = {"fibonacci": [0]}  
result = graph.invoke(initial, config)

# Draw the graph
try:
    graph.get_graph(xray=True).draw_mermaid_png(output_file_path="graph.png")
except Exception:
    pass

# Run the chatbot
n = 0
while True:
    next_fibonacci = fibonacci(n)
    print("Next fibonacci number:", next_fibonacci)

    result = graph.invoke({"fibonacci": [next_fibonacci]}, config)
    print("State: ", result)
    n += 1

    user_input = input(">> ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break