from typing import TypedDict, Annotated
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
import time


class State(TypedDict):
    topics: list[str]
    results: Annotated[list[str], add]


class WorkerState(TypedDict):
    topic: str
    results: Annotated[list[str], add]


def distribute_topics(state: State):
    print("Distrubution.....")
    return [
        Send(
            "research_worker",
            {"topic": topic}
        )
        for topic in state["topics"]
    ]


def research_worker(state: WorkerState):
    print("Research.....")
    time.sleep(2)
    topic = state["topic"]
    return {
        "results": [
            f"Research completed for {topic}"
        ]
    }


builder = StateGraph(State)

builder.add_node("research_worker", research_worker)

builder.add_conditional_edges(START,distribute_topics)
builder.add_edge("research_worker", END)

graph = builder.compile()


result = graph.invoke({
    "topics": ["AI", "Python", "LangGraph"],
    "results": []
})

print(result)