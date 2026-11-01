import time
from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


class subState(TypedDict, total=False):
    number: int
    result: int


class parentState(TypedDict, total=False):
    number: int
    results: Annotated[list[dict], operator.add]


# Three subgraphs

def doubleNumber(state):
    time.sleep(2)
    return {"result": state["number"] * 2}


def tripleNumber(state):
    time.sleep(5)
    return {"result": state["number"] * 3}


def quadrupleNumber(state):
    time.sleep(8)
    return {"result": state["number"] * 4}


def buildSubgraph(function):
    builder = StateGraph(subState)
    builder.add_node("process", function)
    builder.add_edge(START, "process")
    builder.add_edge("process", END)
    return builder.compile()


doubleGraph = buildSubgraph(doubleNumber)
tripleGraph = buildSubgraph(tripleNumber)
quadGraph = buildSubgraph(quadrupleNumber)


# Parent execution nodes

def runDouble(state):
    result = doubleGraph.invoke({"number": state["number"]})
    print("Double completed:", result["result"])
    return {"results": [{"task": "Double", "value": result["result"]}]}


def runTriple(state):
    result = tripleGraph.invoke({"number": state["number"]})
    print("Triple completed:", result["result"])
    return {"results": [{"task": "Triple", "value": result["result"]}]}


def runQuadruple(state):
    result = quadGraph.invoke({"number": state["number"]})
    print("Quadruple completed:", result["result"])
    return {"results": [{"task": "Quadruple", "value": result["result"]}]}


def parallelProcess(state):
    return [
        Send("runDouble", {"number": state["number"]}),
        Send("runTriple", {"number": state["number"]}),
        Send("runQuadruple", {"number": state["number"]})
    ]


# Build parent graph

builder = StateGraph(parentState)

builder.add_node("runDouble", runDouble)
builder.add_node("runTriple", runTriple)
builder.add_node("runQuadruple", runQuadruple)

builder.add_conditional_edges(START, parallelProcess)

builder.add_edge("runDouble", END)
builder.add_edge("runTriple", END)
builder.add_edge("runQuadruple", END)

graph = builder.compile()


# Stream execution updates

for event in graph.stream(
    {"number": 10, "results": []},
    stream_mode="updates"
):
    print("Graph update:", event)