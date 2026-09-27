from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


# ============================================================
# 1. Define the state
# ============================================================

class State(TypedDict):
    message: str
    step1: str
    step2: str
    step3: str


# ============================================================
# 2. Define 3 nodes
# ============================================================

def node1(state: State):
    print("\n========== NODE 1 ==========")

    result = {
        "message": state["message"],
        "step1": "Node 1 completed"
    }

    print("State inside Node 1:")
    print(result)

    return result


def node2(state: State):
    print("\n========== NODE 2 ==========")

    result = {
        "step2": f"Node 2 received: {state['step1']}"
    }

    print("State inside Node 2:")
    print({
        **state,
        **result
    })

    return result


def node3(state: State):
    print("\n========== NODE 3 ==========")

    result = {
        "step3": f"Node 3 received: {state['step2']}"
    }

    print("State inside Node 3:")
    print({
        **state,
        **result
    })

    return result


# ============================================================
# 3. Build graph
# ============================================================

builder = StateGraph(State)

builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)

builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", "node3")
builder.add_edge("node3", END)


# ============================================================
# 4. Create InMemorySaver
# ============================================================

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)


# ============================================================
# 5. Run graph
# ============================================================

config = {
    "configurable": {
        "thread_id": "user123"
    }
}

result = graph.invoke(
    {
        "message": "Hello",
        "step1": "",
        "step2": "",
        "step3": ""
    },
    config=config
)


# ============================================================
# 6. Final result
# ============================================================

print("\n\n========== FINAL RESULT ==========")
print(result)


# ============================================================
# 7. PRINT INMEMORYSAVER CONTENT
# ============================================================

print("\n\n========== SAVED MEMORY ==========")

for checkpoint in checkpointer.list(config):

    print("\n--------------------------------")
    print("Checkpoint ID:")
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