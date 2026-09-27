from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


# --------------------------------------------------
# 1. Define State
# --------------------------------------------------

class State(TypedDict):
    message: str
    step: str


# --------------------------------------------------
# 2. Define Nodes
# --------------------------------------------------

def node_1(state: State):
    print("\n========== NODE 1 ==========")

    new_message = state["message"] + " -> Node 1"

    result = {
        "message": new_message,
        "step": "node_1 completed"
    }

    print("Node 1 state:", result)

    return result


def node_2(state: State):
    print("\n========== NODE 2 ==========")

    new_message = state["message"] + " -> Node 2"

    result = {
        "message": new_message,
        "step": "node_2 completed"
    }

    print("Node 2 state:", result)

    return result


def node_3(state: State):
    print("\n========== NODE 3 ==========")

    new_message = state["message"] + " -> Node 3"

    result = {
        "message": new_message,
        "step": "node_3 completed"
    }

    print("Node 3 state:", result)

    return result


# --------------------------------------------------
# 3. Create Graph
# --------------------------------------------------

builder = StateGraph(State)

builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)


# --------------------------------------------------
# 4. Create InMemorySaver
# --------------------------------------------------

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)


# --------------------------------------------------
# 5. Thread configuration
# --------------------------------------------------

config = {
    "configurable": {
        "thread_id": "user123"
    }
}


# --------------------------------------------------
# 6. Run graph
# --------------------------------------------------

result = graph.invoke(
    {
        "message": "Hello",
        "step": "starting"
    },
    config
)


# --------------------------------------------------
# 7. Final result
# --------------------------------------------------

print("\n\n========== FINAL RESULT ==========")
print(result)


# --------------------------------------------------
# 8. Print EVERYTHING saved by InMemorySaver
# --------------------------------------------------

print("\n\n========== SAVED MEMORY ==========")

for i, checkpoint in enumerate(checkpointer.list(config), 1):

    print(f"\n--- Checkpoint {i} ---")

    print("Thread ID:")
    print(
        checkpoint.config["configurable"]["thread_id"]
    )

    print("\nCheckpoint ID:")
    print(
        checkpoint.config["configurable"]["checkpoint_id"]
    )

    print("\nSaved state:")
    print(
        checkpoint.checkpoint["channel_values"]
    )

    print("\nMetadata:")
    print(
        checkpoint.metadata
    )
print("==" * 75 )
print(checkpointer.list(config))