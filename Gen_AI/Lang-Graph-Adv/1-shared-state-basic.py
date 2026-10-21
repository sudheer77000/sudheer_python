from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    count: int
    result: str

# Subgraph nodes
def increment(state: State):
    return {"count": state["count"] + 1}

def format_result(state: State):
    return {"result": f"Count is {state['count']}"}

sub_builder = StateGraph(State)

sub_builder.add_node("increment", increment)
sub_builder.add_node("format", format_result)

sub_builder.add_edge(START, "increment")
sub_builder.add_edge("increment", "format")
sub_builder.add_edge("format", END)

subgraph = sub_builder.compile()

# Parent graph
parent_builder = StateGraph(State)
parent_builder.add_node("subgraph", subgraph)
parent_builder.add_node(
    "finish",
    lambda state: {
        "result": state["result"] + " — finished"
    },
)
parent_builder.add_edge(START, "subgraph")
parent_builder.add_edge("subgraph", "finish")
parent_builder.add_edge("finish", END)

graph = parent_builder.compile()

print(graph.invoke({"count": 0, "result": ""}))