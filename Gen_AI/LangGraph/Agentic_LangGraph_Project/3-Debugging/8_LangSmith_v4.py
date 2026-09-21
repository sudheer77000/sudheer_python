import os
import logging
from typing import TypedDict
from langsmith import Client
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

# 1. Enable console logging for LangSmith tracing
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logging.getLogger("langsmith").setLevel(logging.DEBUG)

# 2. Configure LangSmith Tracing and EU Endpoint Environment Variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "langgraph-learning"
os.environ["LANGCHAIN_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"

# Initialize LangSmith client for flushing traces
client = Client()


# 3. Define the graph state
class State(TypedDict):
  counter: int
  message: str


# 4. Define node functions that update the state
def increment_node(state: State):
  return {"counter": state["counter"] + 1, "message": "Incremented by 1"}


def double_node(state: State):
  return {"counter": state["counter"] * 2, "message": "Doubled the counter"}


def triple_node(state: State):
  return {"counter": state["counter"] * 3, "message": "Triple the counter"}


def quadruple_Node(state: State):
  return {"counter": state["counter"] * 4, "message": "Quadruple the counter"}


# 5. Build the graph structure
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

# 6. Compile the graph properly with parentheses ()
# (LangGraph platform handles persistence automatically, so no checkpointer is needed here)
app = workflow.compile()

# 7. Define a thread configuration (thread_id isolates this execution session)
config = {"configurable": {"thread_id": "session_abc_123"}}

if __name__ == "__main__":
  # Run the graph for the first time
  print("--- Running the Graph (Tracing Enabled) ---")
  initial_input = {"counter": 5, "message": "Starting state"}
  result = app.invoke(initial_input, config=config)
  print("Result Output:", result)

  # Force flush any pending background traces to the EU server
  client.flush()

  # 8. Retrieve and print ALL state snapshots across every edge
  print("\n--- Inspecting All State Snapshots Across Edges ---")
  snapshots = list(app.get_state_history(config))[::-1]

  for idx, snapshot in enumerate(snapshots):
    print(f"\n--- Snapshot Step {idx} ---")
    print(f"Step metadata: {snapshot.metadata}")
    print(f"Values (.values): {snapshot.values}")
    print(f"Next Node (.next): {snapshot.next}")
    print("-" * 50)