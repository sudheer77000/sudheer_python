
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
import operator

from rich.console import Console
from rich.table import Table
from rich import box


# ================= STATE DEFINITIONS =================

class parentState(TypedDict, total=False):
    nameAgeList: list[dict]
    results: Annotated[list[dict], operator.add]


class childState(TypedDict, total=False):
    name: str
    age: int
    classification: str


# ================= CHILD GRAPH =================

def ageClassification(state: childState):

    age = state["age"]

    if age < 13:
        classification = "Child"
    elif age < 20:
        classification = "Teenager"
    elif age < 60:
        classification = "Adult"
    else:
        classification = "Senior Citizen"

    return {
        "name": state["name"],
        "age": age,
        "classification": classification
    }


# Build Child Graph

childBuilder = StateGraph(childState)

childBuilder.add_node("ageClassification", ageClassification)

childBuilder.add_edge(START, "ageClassification")
childBuilder.add_edge("ageClassification", END)

childGraph = childBuilder.compile()


# ================= PARENT GRAPH =================

console = Console()


# 1. Print input data

def printNameAge(state: parentState):

    table = Table(
        title="Person Details",
        box=box.ROUNDED,
        header_style="bold cyan",
        title_style="bold white"
    )

    table.add_column("Name", style="bold green")
    table.add_column("Age", justify="center", style="bold yellow")

    for person in state["nameAgeList"]:
        table.add_row(
            person["name"],
            str(person["age"])
        )

    console.print(table)

    return {}


# 2. Fan-out: Send each person to child graph

def callChildGraphs(state: parentState):

    return [
        Send("childGraph", person)
        for person in state["nameAgeList"]
    ]


# 3. Execute child graph

def executeChildGraph(state: childState):

    result = childGraph.invoke(state)

    return {
        "results": [result]
    }


# 4. Display final classification results

def displayResults(state: parentState):

    table = Table(
        title="Age Classification Results",
        box=box.ROUNDED,
        header_style="bold cyan",
        title_style="bold white"
    )

    table.add_column("Name", style="bold green")
    table.add_column("Age", justify="center", style="bold yellow")
    table.add_column("Classification", style="bold magenta")

    for person in state["results"]:
        table.add_row(
            person["name"],
            str(person["age"]),
            person["classification"]
        )

    console.print(table)

    return {}


# ================= BUILD PARENT GRAPH =================

parentBuilder = StateGraph(parentState)

parentBuilder.add_node("printNameAge", printNameAge)
parentBuilder.add_node("childGraph",executeChildGraph)
parentBuilder.add_node("displayResults",displayResults)

# Normal flow
parentBuilder.add_edge(START, "printNameAge")
parentBuilder.add_conditional_edges("printNameAge",callChildGraphs,["childGraph"])
parentBuilder.add_edge("childGraph", "displayResults")
parentBuilder.add_edge("displayResults", END)

parentGraph = parentBuilder.compile()


# ================= MAIN GRAPH INVOKE =================

input_data = [
    {"name": "Sudheer", "age": 29},
    {"name": "Arun", "age": 40},
    {"name": "Sunil", "age": 38},
    {"name": "Rahul", "age": 10},
    {"name": "Kiran", "age": 16},
    {"name": "Ramesh", "age": 65}
]

result = parentGraph.invoke({
    "nameAgeList": input_data
})

print("\nFinal Graph Output:")
print(result)
