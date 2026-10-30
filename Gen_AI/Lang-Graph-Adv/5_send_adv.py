
from typing import TypedDict, Annotated
import operator
import time

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


# Print text one word at a time
def type_words(message, delay=1, style="cyan"):
    for word in message.split():
        console.print(word, end=" ", style=style)
        time.sleep(delay)
    console.print()


# Parent graph state
class ParentState(TypedDict):
    transactions: list[dict]
    results: Annotated[list[dict], operator.add]


# Subgraph state
class FraudState(TypedDict):
    account: str
    amount: int
    results: list[dict]


# Fraud checking worker
def check_fraud(state: FraudState):
    amount = state["amount"]

    if amount >= 10000:
        status = "Rejected"
    elif amount >= 1000:
        status = "Review"
    else:
        status = "Approved"

    return {
        "results": [{
            "account": state["account"],
            "status": status
        }]
    }


# Build subgraph
sub = StateGraph(FraudState)
sub.add_node("check", check_fraud)
sub.add_edge(START, "check")
sub.add_edge("check", END)

fraud_subgraph = sub.compile()


# Dispatch transactions to parallel workers
def dispatch(state: ParentState):
    return [
        Send("fraud", {
            "account": tx["account"],
            "amount": tx["amount"],
            "results": []
        })
        for tx in state["transactions"]
    ]


# Build parent graph
parent = StateGraph(ParentState)
parent.add_node("fraud", fraud_subgraph)
parent.add_conditional_edges(START, dispatch)
parent.add_edge("fraud", END)

graph = parent.compile()


# Input: 50 sample transactions
transactions = [
    {"account": "A1001", "amount": 200},
    {"account": "A1002", "amount": 2000},
    {"account": "A1003", "amount": 500},
    {"account": "A1004", "amount": 10000},
    {"account": "A1005", "amount": 750},
    {"account": "A1006", "amount": 12000},
    {"account": "A1007", "amount": 100},
    {"account": "A1008", "amount": 850},
    {"account": "A1009", "amount": 10000},
    {"account": "A1010", "amount": 600},
    {"account": "A1011", "amount": 1200},
    {"account": "A1012", "amount": 350},
    {"account": "A1013", "amount": 2800},
    {"account": "A1014", "amount": 900},
    {"account": "A1015", "amount": 150},
    {"account": "A1016", "amount": 15000},
    {"account": "A1017", "amount": 400},
    {"account": "A1018", "amount": 1750},
    {"account": "A1019", "amount": 650},
    {"account": "A1020", "amount": 1100},
    {"account": "A1021", "amount": 250},
    {"account": "A1022", "amount": 10000},
    {"account": "A1023", "amount": 700},
    {"account": "A1024", "amount": 2200},
    {"account": "A1025", "amount": 550},
    {"account": "A1026", "amount": 950},
    {"account": "A1027", "amount": 18000},
    {"account": "A1028", "amount": 300},
    {"account": "A1029", "amount": 1350},
    {"account": "A1030", "amount": 800},
    {"account": "A1031", "amount": 180},
    {"account": "A1032", "amount": 2600},
    {"account": "A1033", "amount": 625},
    {"account": "A1034", "amount": 1450},
    {"account": "A1035", "amount": 10000},
    {"account": "A1036", "amount": 320},
    {"account": "A1037", "amount": 980},
    {"account": "A1038", "amount": 3100},
    {"account": "A1039", "amount": 475},
    {"account": "A1040", "amount": 1250},
    {"account": "A1041", "amount": 220},
    {"account": "A1042", "amount": 25000},
    {"account": "A1043", "amount": 720},
    {"account": "A1044", "amount": 1650},
    {"account": "A1045", "amount": 890},
    {"account": "A1046", "amount": 10000},
    {"account": "A1047", "amount": 150},
    {"account": "A1048", "amount": 3600},
    {"account": "A1049", "amount": 580},
    {"account": "A1050", "amount": 1050},
]


# Display animated heading
console.print()

console.print(
    Panel(
        Text(
            "BANK FRAUD MONITOR",
            justify="center",
            style="bold white"
        ),
        border_style="bright_blue",
        box=box.DOUBLE
    )
)

type_words(
    "Initializing fraud detection system...",
    delay=0.3,
    style="cyan"
)

type_words(
    "Analyzing incoming transactions...",
    delay=0.3,
    style="yellow"
)


# Execute LangGraph
result = graph.invoke({
    "transactions": transactions,
    "results": []
})


# Sort results into account-number order for display
results = sorted(
    result["results"],
    key=lambda item: item["account"]
)


# Print each result word by word
for item in results:
    account = item["account"]
    status = item["status"]

    if status == "Approved":
        style = "bold green"
        symbol = "✓"
    elif status == "Review":
        style = "bold yellow"
        symbol = "!"
    else:
        style = "bold red"
        symbol = "✗"

    type_words(
        f"{symbol} Account {account} status {status}",
        delay=0.3,
        style=style
    )


# Create final results table
table = Table(
    title="Transaction Analysis Results",
    box=box.ROUNDED,
    header_style="bold cyan",
    title_style="bold white",
    show_lines=True
)

table.add_column("Account Number", style="white")
table.add_column("Status", justify="center")
table.add_column("Result", justify="center")


# Add every result to the table
for item in results:
    account = item["account"]
    status = item["status"]

    if status == "Approved":
        status_style = "[bold green]APPROVED[/bold green]"
        icon = "[green]✓[/green]"

    elif status == "Review":
        status_style = "[bold yellow]REVIEW[/bold yellow]"
        icon = "[yellow]![/yellow]"

    else:
        status_style = "[bold red]REJECTED[/bold red]"
        icon = "[bold red]✗[/bold red]"

    # Important: add_row must be inside the loop
    table.add_row(
        account,
        status_style,
        icon
    )


# Print final table
console.print()
console.print(table)


# Count each status
approved_count = sum(
    item["status"] == "Approved" for item in results
)

review_count = sum(
    item["status"] == "Review" for item in results
)

rejected_count = sum(
    item["status"] == "Rejected" for item in results
)


# Final summary
summary = (
    f"[bold green]Approved:[/bold green] {approved_count}\n"
    f"[bold yellow]Review:[/bold yellow] {review_count}\n"
    f"[bold red]Rejected:[/bold red] {rejected_count}\n"
    f"[bold white]Total processed:[/bold white] {len(results)}"
)

console.print(
    Panel(
        summary,
        border_style="bright_blue",
        title="[bold cyan]Analysis Summary[/bold cyan]",
        box=box.ROUNDED
    )
)
