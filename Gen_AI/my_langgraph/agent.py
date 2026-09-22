from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# State
class State(TypedDict):
    message: str


# Node
def hello_node(state: State):
    return {
        "message": "Hello " + state["message"]
    }


# Build graph
builder = StateGraph(State)

builder.add_node("hello", hello_node)

builder.add_edge(START, "hello")
builder.add_edge("hello", END)

# Compile
graph = builder.compile()