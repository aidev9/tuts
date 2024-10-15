'''
    We will start with a simple graph where a single Developer node connected to START and END nodes.

    The StateGraph will be created with a TypedDict and have a single entry point and an edge to the end node. It will consist of a single key "count" with an initial value of 0.

    The Developer node will increment the count by 1 and return the state.

    We will add memory to the graph to save the state of the graph.

    Then, we will create a visualization of the graph.

    Finally, we will run the graph and print the result.
'''

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Define state
class GraphState(TypedDict):
    count: int

# Create the graph
builder = StateGraph(GraphState)

# Create developer node
def developer(state):
    print('------ Developer ------')
    state['count'] += 1  # Increment the count
    return state  # Return the modified state

# Add the node to the graph
builder.add_node("developer", developer)

# Set entry point and edges
builder.add_edge(START, "developer")
builder.add_edge('developer', END)

# Configuration and memory
config = {"configurable": {"thread_id": 1}}
memory = MemorySaver()

# Compile and run the builder
graph = builder.compile(checkpointer=memory)
inputs = {"count": 0}  # Provide the initial state
result = graph.invoke(inputs, config)
print(result)

# Draw the graph
try:
    graph.get_graph(xray=True).draw_mermaid_png(output_file_path="graph.png")
except Exception:
    pass

# Run the chatbot
while True:
    user_input = input(">> ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    
    count = graph.get_state(config).values["count"]
    result = graph.invoke({"count": count}, config)
    print(result)