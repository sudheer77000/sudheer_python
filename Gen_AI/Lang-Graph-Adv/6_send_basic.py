from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
import operator
from rich.console import Console
from rich.table import Table
from rich import box

class parentState(TypedDict, total=False):
    nameAgeList : list[dict]
    results: Annotated[list[dict], operator.add]

class childState(TypedDict, total=False):
    name: str
    age: int
    classification: str

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
        "classification": classification
    }

# Build Child graph
childBuilder = StateGraph(childState)
childBuilder.add_node("ageClassification", ageClassification)

childBuilder.add_edge(START, "ageClassification")
childBuilder.add_edge("ageClassification", END)
childGraph = childBuilder.compile()

# Parent Graph

console = Console()

def printNameAge(state: parentState):

    table = Table(
        title="Person Details",
        box=box.ROUNDED,
        header_style="bold cyan",
        title_style="bold white"
    )

    table.add_column("Name", style="bold green")
    table.add_column("Age", justify="center", style="bold yellow")
    print("=" * 60)
    print("---- MainGraph ----")
    for person in state['nameAgeList']:
        table.add_row(
            person['name'],
            str(person['age'])
        )
    console.print(table)
print("=" * 60)
# Build Parent graph
parentBuilder = StateGraph(parentState)
parentBuilder.add_node("printNameAge", printNameAge)

parentBuilder.add_edge(START, "printNameAge")
parentBuilder.add_edge("printNameAge", END)

parentGraph = parentBuilder.compile()

# =================SubGraph Invoke ==========

child_input_data = {"name": "Sudheer", "age": 38}

result = childGraph.invoke(child_input_data)

print("=" * 10)
print("---- SubGraph ----")
print(result)
print("=" * 20)
# =================Main Graph Invoke ==========

# Input
input_data = [
    {"name": "Sudheer", "age": 29},
    {"name": "Arun", "age": 40},
    {"name": "Sunil", "age": 38}
]


# Execute
parentGraph.invoke({
    "nameAgeList": input_data
})