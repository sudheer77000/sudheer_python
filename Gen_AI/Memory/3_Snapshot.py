from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# 1. Define the graph state
class State(TypedDict):
    counter: int
    message: str

# 2. Define node functions that update the state
def increment_node(state: State):
    return {"counter": state["counter"] + 1, "message": "Incremented by 1"}

def double_node(state: State):
    return {"counter": state["counter"] * 2, "message": "Doubled the counter"}

def triple_node(state: State):
    return {"counter": state["counter"] * 3, "message": "Triple the counter"}

def quadruple_Node(state: State):
    return {"counter": state["counter"] * 4, "message": "Quadruple the counter"}

# 3. Build the graph structure
workflow = StateGraph(State)

workflow.add_node("increment", increment_node)
workflow.add_node("double", double_node)
workflow.add_node("triple", triple_node)
workflow.add_node("quadruple", quadruple_Node)

# Define the execution flow
workflow.set_entry_point("increment")
workflow.add_edge("increment", "double")
workflow.add_edge("double", "triple")
workflow.add_edge("triple", "quadruple")
workflow.add_edge("quadruple", END)

# 4. Initialize MemorySaver and compile the graph
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# 5. Define a thread configuration (thread_id isolates this execution session)
config = {"configurable": {"thread_id": "session_abc_123"}}

# Run the graph for the first time
print("--- Running the Graph ---")
initial_input = {"counter": 5, "message": "Starting state"}
result = app.invoke(initial_input, config=config)
print("Result Output:", result)

# 6. Retrieve and print ALL state snapshots across every edge
print("\n--- Inspecting All State Snapshots Across Edges ---")

# get_state_history yields snapshots from newest to oldest.
# Using list()[::-1] prints them chronologically (Step 0 -> Step 4).
snapshots = list(app.get_state_history(config))[::-1]
print(snapshots)

# for idx, snapshot in enumerate(snapshots):
#     print(f"\n--- Snapshot Step {idx} ---")
#     print(f"Step: {snapshot.metadata.get('step')}")
#     print(f"Source Node: {snapshot.metadata.get('source')}")
#     print(f"Values (.values): {snapshot.values}")
#     print(f"Next Node (.next): {snapshot.next}")
#     print(f"Checkpoint ID: {snapshot.config['configurable']['checkpoint_id']}")
#     print("-" * 50)
#     print(snapshot)