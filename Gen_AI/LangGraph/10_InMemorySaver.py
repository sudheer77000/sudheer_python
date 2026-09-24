from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict):
    message: str


def my_node(state: State):
    return {
        "message": state["message"] + " - processed"
    }


# Create graph
builder = StateGraph(State)

builder.add_node("my_node", my_node)

builder.add_edge(START, "my_node")
builder.add_edge("my_node", END)


# Create checkpoint saver
checkpointer = InMemorySaver()

# Compile graph with checkpointing
graph = builder.compile(
    checkpointer=checkpointer
)


# First run
result1 = graph.invoke(
    {"message": "Hello"},
    config={
        "configurable": {
            "thread_id": "user123"
        }
    }
)

print("First result:", result1)


# Second run using the SAME thread_id
result2 = graph.invoke(
    {"message": "How are you?"},
    config={
        "configurable": {
            "thread_id": "user123"
        }
    }
)

print("Second result:", result2)


# Inspect memory
print("\nSaved checkpoints:")

for checkpoint in checkpointer.list(
    {"configurable": {"thread_id": "user123"}}
):
    print(checkpoint.checkpoint["channel_values"])