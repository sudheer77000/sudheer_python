from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    name: str
    result1: str
    result2: str


def task1(state: State):
    return {"result1": f"Hello {state['name']}!"}


def task2(state: State):
    return {"result2": f"Welcome {state['name']}!"}


builder = StateGraph(State)

builder.add_node("task1", task1)
builder.add_node("task2", task2)

# Both start after START
builder.add_edge(START, "task1")
builder.add_edge(START, "task2")

builder.add_edge("task1", END)
builder.add_edge("task2", END)

graph = builder.compile()

result = graph.invoke({
    "name": "Sudheer",
    "result1": "",
    "result2": ""
})

print(result)