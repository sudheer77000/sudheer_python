
from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send


# -------------------------------
# 1. State Definitions
# -------------------------------

class subState(TypedDict, total=False):
    number: int
    result: int


class parentState(TypedDict, total=False):
    number: int
    results: Annotated[list[dict], operator.add]
    total: int


# -------------------------------
# 2. Subgraph 1: Double
# -------------------------------

def doubleNumber(state: subState):
    return {"result": state["number"] * 2}


doubleBuilder = StateGraph(subState)
doubleBuilder.add_node("doubleNumber", doubleNumber)
doubleBuilder.add_edge(START, "doubleNumber")
doubleBuilder.add_edge("doubleNumber", END)

doubleGraph = doubleBuilder.compile()


# -------------------------------
# 3. Subgraph 2: Triple
# -------------------------------

def tripleNumber(state: subState):
    return {"result": state["number"] * 3}


tripleBuilder = StateGraph(subState)
tripleBuilder.add_node("tripleNumber", tripleNumber)
tripleBuilder.add_edge(START, "tripleNumber")
tripleBuilder.add_edge("tripleNumber", END)

tripleGraph = tripleBuilder.compile()


# -------------------------------
# 4. Subgraph 3: Quadruple
# -------------------------------

def quadrupleNumber(state: subState):
    return {"result": state["number"] * 4}


quadBuilder = StateGraph(subState)
quadBuilder.add_node("quadrupleNumber", quadrupleNumber)
quadBuilder.add_edge(START, "quadrupleNumber")
quadBuilder.add_edge("quadrupleNumber", END)

quadGraph = quadBuilder.compile()


# -------------------------------
# 5. Parent Graph: Execute Subgraphs
# -------------------------------

def runDouble(state: subState):

    result = doubleGraph.invoke({
        "number": state["number"]
    })

    return {
        "results": [{
            "task": "Double",
            "value": result["result"]
        }]
    }


def runTriple(state: subState):

    result = tripleGraph.invoke({
        "number": state["number"]
    })

    return {
        "results": [{
            "task": "Triple",
            "value": result["result"]
        }]
    }


def runQuadruple(state: subState):

    result = quadGraph.invoke({
        "number": state["number"]
    })

    return {
        "results": [{
            "task": "Quadruple",
            "value": result["result"]
        }]
    }


# -------------------------------
# 6. Parallel Fan-out using Send
# -------------------------------

def parallelProcess(state: parentState):

    return [
        Send("runDouble", {"number": state["number"]}),
        Send("runTriple", {"number": state["number"]}),
        Send("runQuadruple", {"number": state["number"]})
    ]


# -------------------------------
# 7. Add All Results
# -------------------------------

def addResults(state: parentState):

    total = sum(item["value"] for item in state["results"])

    return {"total": total}


# -------------------------------
# 8. Build Parent Graph
# -------------------------------

parentBuilder = StateGraph(parentState)

parentBuilder.add_node("runDouble", runDouble)
parentBuilder.add_node("runTriple", runTriple)
parentBuilder.add_node("runQuadruple", runQuadruple)

parentBuilder.add_node("addResults", addResults)

parentBuilder.add_conditional_edges(
    START,
    parallelProcess
)

# All parallel branches converge on addResults
parentBuilder.add_edge("runDouble", "addResults")
parentBuilder.add_edge("runTriple", "addResults")
parentBuilder.add_edge("runQuadruple", "addResults")

parentBuilder.add_edge("addResults", END)

parentGraph = parentBuilder.compile()


# -------------------------------
# 9. Execute Parent Graph
# -------------------------------

result = parentGraph.invoke({
    "number": 10,
    "results": []
})

print("Individual Results:")

for item in result["results"]:
    print(item["task"], ":", item["value"])

print("Total:", result["total"])
