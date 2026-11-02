
from typing import TypedDict, Annotated
from operator import or_
from langgraph.graph import StateGraph, START, END
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich import box

console = Console()


# =====================================================
# 1. SHARED STATE
# =====================================================

class BankState(TypedDict):
    customer_request: str
    tasks: list
    current_task: str
    current_team: str
    results: Annotated[dict, or_]
    completed: bool
    final_response: str


# =====================================================
# 2. WORKER AGENTS
# =====================================================

def balance_agent(state):
    console.print("[cyan]    -> Balance Agent working...[/cyan]")

    return {
        "results": {
            "balance": "Available balance: AED 15,000"
        }
    }


def transaction_agent(state):
    console.print("[cyan]    -> Transaction Agent working...[/cyan]")

    return {
        "results": {
            "transactions": (
                "Last 5 transactions retrieved. "
                "No unusual spending pattern detected."
            )
        }
    }


def limit_agent(state):
    console.print("[cyan]    -> Card Limit Agent working...[/cyan]")

    return {
        "results": {
            "card_limit": (
                "Limit increase eligibility can be checked. "
                "Customer approval and bank authorization "
                "are required before changing the limit."
            )
        }
    }


def international_card_agent(state):
    console.print(
        "[cyan]    -> International Card Agent working...[/cyan]"
    )

    return {
        "results": {
            "international": (
                "International card usage is supported, "
                "subject to card settings and issuer restrictions."
            )
        }
    }


def identity_agent(state):
    console.print("[cyan]    -> Identity Verification Agent working...[/cyan]")

    return {
        "results": {
            "identity": (
                "Additional identity verification is required "
                "before sensitive banking operations."
            )
        }
    }


def fraud_agent(state):
    console.print("[cyan]    -> Fraud Detection Agent working...[/cyan]")

    return {
        "results": {
            "fraud": "No suspicious activity found in this simulation."
        }
    }


def travel_notice_agent(state):
    console.print("[cyan]    -> Travel Notice Agent working...[/cyan]")

    return {
        "results": {
            "travel": (
                "Travel notification can be prepared. "
                "Customer confirmation is required before submission."
            )
        }
    }


def currency_agent(state):
    console.print("[cyan]    -> Foreign Currency Agent working...[/cyan]")

    return {
        "results": {
            "currency": (
                "Foreign exchange information can be retrieved "
                "from the bank's authorized currency service."
            )
        }
    }


# =====================================================
# 3. SUB-SUPERVISOR FACTORY
# =====================================================

def create_department(name, workers):

    department = StateGraph(BankState)

    def department_supervisor(state):
        task = state["current_task"]

        console.print(
            f"[yellow]  {name} Supervisor delegates: "
            f"{task}[/yellow]"
        )

        return {}

    def choose_worker(state):
        return state["current_task"]

    department.add_node(
        "department_supervisor",
        department_supervisor
    )

    for worker_name, worker_function in workers.items():
        department.add_node(worker_name, worker_function)

    department.add_edge(START, "department_supervisor")

    department.add_conditional_edges(
        "department_supervisor",
        choose_worker,
        {worker: worker for worker in workers}
    )

    for worker in workers:
        department.add_edge(worker, END)

    return department.compile()


# =====================================================
# 4. CREATE DEPARTMENT HIERARCHY
# =====================================================

account_supervisor = create_department(
    "Account",
    {
        "balance": balance_agent,
        "transactions": transaction_agent
    }
)

card_supervisor = create_department(
    "Card",
    {
        "card_limit": limit_agent,
        "international": international_card_agent
    }
)

security_supervisor = create_department(
    "Security",
    {
        "identity": identity_agent,
        "fraud": fraud_agent
    }
)

travel_supervisor = create_department(
    "Travel Support",
    {
        "travel": travel_notice_agent,
        "currency": currency_agent
    }
)


# =====================================================
# 5. MAIN SUPERVISOR - TASK PLANNING
# =====================================================

def task_planner(state):

    request = state["customer_request"].lower()

    tasks = []

    # Account department
    if "balance" in request:
        tasks.append({
            "id": "balance",
            "team": "account"
        })

    if any(word in request for word in
           ["transaction", "spending", "payment"]):
        tasks.append({
            "id": "transactions",
            "team": "account"
        })

    # Card department
    if any(word in request for word in
           ["limit", "increase"]):
        tasks.append({
            "id": "card_limit",
            "team": "card"
        })

    if any(word in request for word in
           ["international", "abroad", "overseas", "travel"]):
        tasks.append({
            "id": "international",
            "team": "card"
        })

    # Security department
    if any(word in request for word in
           ["limit", "increase", "travel", "abroad",
            "international", "transfer"]):
        tasks.append({
            "id": "identity",
            "team": "security"
        })

    # Run security screening for the request
    if tasks:
        tasks.append({
            "id": "fraud",
            "team": "security"
        })

    # Travel support department
    if any(word in request for word in
           ["travel", "travelling", "abroad", "trip"]):
        tasks.append({
            "id": "travel",
            "team": "travel"
        })

    if any(word in request for word in
           ["currency", "exchange", "foreign"]):
        tasks.append({
            "id": "currency",
            "team": "travel"
        })

    if not tasks:
        tasks.append({
            "id": "balance",
            "team": "account"
        })

    console.print(
        Panel(
            "\n".join(
                f"• {task['team'].title()}: {task['id']}"
                for task in tasks
            ),
            title="[bold green]Main Supervisor - Execution Plan[/bold green]",
            border_style="green"
        )
    )

    return {"tasks": tasks}


# =====================================================
# 6. MAIN SUPERVISOR - DELEGATION
# =====================================================

def main_supervisor(state):

    if not state["tasks"]:
        console.print(
            "[bold green]Main Supervisor: "
            "All departments completed their work.[/bold green]"
        )

        return {"completed": True}

    task = state["tasks"][0]

    console.print(
        Panel(
            f"Delegating task: [bold]{task['id']}[/bold]\n"
            f"Department: [bold]{task['team']}[/bold]",
            title="[bold blue]Main Supervisor[/bold blue]",
            border_style="blue"
        )
    )

    return {
        "tasks": state["tasks"][1:],
        "current_task": task["id"],
        "current_team": task["team"],
        "completed": False
    }


def route_department(state):
    if state["completed"]:
        return "final_report"

    return state["current_team"]


# =====================================================
# 7. FINAL SUPERVISOR - CONSOLIDATION
# =====================================================

def final_supervisor(state):

    console.print(
        "\n[bold green]Main Supervisor: "
        "Consolidating department reports...[/bold green]"
    )

    response = "\n".join(
        f"• {key.replace('_', ' ').title()}: {value}"
        for key, value in state["results"].items()
    )

    return {"final_response": response}


# =====================================================
# 8. BUILD HIERARCHICAL LANGGRAPH
# =====================================================

bank_graph = StateGraph(BankState)

bank_graph.add_node("planner", task_planner)
bank_graph.add_node("main_supervisor", main_supervisor)

bank_graph.add_node("account", account_supervisor)
bank_graph.add_node("card", card_supervisor)
bank_graph.add_node("security", security_supervisor)
bank_graph.add_node("travel", travel_supervisor)

bank_graph.add_node("final_report", final_supervisor)

bank_graph.add_edge(START, "planner")
bank_graph.add_edge("planner", "main_supervisor")

bank_graph.add_conditional_edges(
    "main_supervisor",
    route_department,
    {
        "account": "account",
        "card": "card",
        "security": "security",
        "travel": "travel",
        "final_report": "final_report"
    }
)

# Every department returns control to Main Supervisor
for department in [
    "account", "card", "security", "travel"
]:
    bank_graph.add_edge(department, "main_supervisor")

bank_graph.add_edge("final_report", END)

app = bank_graph.compile()


# =====================================================
# 9. DISPLAY ARCHITECTURE USING RICH
# =====================================================

def show_architecture():

    tree = Tree("[bold blue]Main Supervisor[/bold blue]")

    teams = {
        "Account Supervisor": [
            "Balance Agent",
            "Transaction Agent"
        ],
        "Card Supervisor": [
            "Card Limit Agent",
            "International Card Agent"
        ],
        "Security Supervisor": [
            "Identity Verification Agent",
            "Fraud Detection Agent"
        ],
        "Travel Support Supervisor": [
            "Travel Notice Agent",
            "Foreign Currency Agent"
        ]
    }

    for supervisor, agents in teams.items():
        branch = tree.add(f"[yellow]{supervisor}[/yellow]")

        for agent in agents:
            branch.add(f"[cyan]{agent}[/cyan]")

    console.print(
        Panel(
            tree,
            title="[bold]BANKING MULTI-AGENT ARCHITECTURE[/bold]",
            border_style="blue"
        )
    )


# =====================================================
# 10. RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    console.print(
        Panel(
            "[bold white]WELCOME TO AI BANKING SYSTEM[/bold white]",
            style="blue"
        )
    )

    show_architecture()

    customer_request = input(
        "\nEnter your banking request: "
    )

    initial_state = {
        "customer_request": customer_request,
        "tasks": [],
        "current_task": "",
        "current_team": "",
        "results": {},
        "completed": False,
        "final_response": ""
    }

    console.print(
        "\n[bold blue]Starting Hierarchical Supervisor...[/bold blue]\n"
    )

    result = app.invoke(initial_state)

    # Display final results
    table = Table(
        title="Banking Operations Summary",
        box=box.ROUNDED
    )

    table.add_column("Department Task", style="cyan")
    table.add_column("Agent Result", style="green")

    for key, value in result["results"].items():
        table.add_row(key.replace("_", " ").title(), value)

    console.print(table)

    console.print(
        Panel(
            result["final_response"],
            title="[bold green]FINAL CUSTOMER RESPONSE[/bold green]",
            border_style="green"
        )
    )

    console.print(
        "\n[bold green]Banking workflow completed![/bold green]"
    )
