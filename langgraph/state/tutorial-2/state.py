'''
    In this second example, we will create a simple graph that will hold a list of the Fibonacci numbers.
    Our StateGraph will use TypedDict and have a single entry point and an edge to the end node. It will consist of a single key "fibonacci" with an initial value of [0].
    The fibonacci_reducer function will be used to update the state by adding the next Fibonacci number to the list.
    The state will be updated by the custom reducer, while the Developer node will be a noop. In the chatbot loop we will manually calculate the next Fibonacci number and pass it to the graph.
    We will add memory to the graph to save the state of the graph.
    We will draw a visualization of the graph. In addition, we will utilize LangSmith to trace the execution of the graph and monitor the state changes.
    Finally, we will run the graph and print the result.
'''

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated

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
config = {"configurable": {"thread_id": 1}}
memory = MemorySaver()

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