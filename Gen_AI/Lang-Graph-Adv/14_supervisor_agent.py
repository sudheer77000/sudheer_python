
from typing import TypedDict, Literal

from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()


console = Console()


# =====================================
# 1. Initialize OpenAI
# =====================================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# =====================================
# 2. Define Routing Schema
# =====================================

class RouteDecision(BaseModel):
    category: Literal[
        "technical",
        "billing",
        "general"
    ]


# =====================================
# 3. Define Shared State
# =====================================

class AgentState(TypedDict):
    question: str
    category: str
    specialist_response: str
    final_answer: str


# =====================================
# 4. Supervisor Agent
# =====================================

router_llm = llm.with_structured_output(RouteDecision)


def supervisor(state: AgentState):

    result = router_llm.invoke([
        (
            "system",
            """
            You are a Supervisor Agent.

            Analyze the user's question and select exactly
            one specialized agent.

            Technical:
            Software, programming, APIs, errors,
            databases and troubleshooting.

            Billing:
            Payments, invoices, refunds,
            subscriptions and pricing.

            General:
            All other questions.

            Return the correct category.
            """
        ),
        ("human", state["question"])
    ])

    console.print(
        f"\n[bold magenta]Supervisor selected:[/bold magenta] "
        f"{result.category.upper()}"
    )

    return {
        "category": result.category
    }


# =====================================
# 5. Technical Agent
# =====================================

def technical_agent(state: AgentState):

    response = llm.invoke([
        (
            "system",
            """
            You are a Technical Support Specialist.

            Help users with:
            - Programming
            - Software errors
            - APIs
            - Databases
            - Technical troubleshooting

            Provide clear and practical solutions.
            """
        ),
        ("human", state["question"])
    ])

    return {
        "specialist_response": response.content
    }


# =====================================
# 6. Billing Agent
# =====================================

def billing_agent(state: AgentState):

    response = llm.invoke([
        (
            "system",
            """
            You are a Billing Support Specialist.

            Help users with:
            - Payment issues
            - Invoices
            - Refunds
            - Subscriptions
            - Billing questions

            Never claim that a payment or refund
            has been processed unless verified.
            """
        ),
        ("human", state["question"])
    ])

    return {
        "specialist_response": response.content
    }


# =====================================
# 7. General Agent
# =====================================

def general_agent(state: AgentState):

    response = llm.invoke([
        (
            "system",
            """
            You are a General Customer Support Specialist.

            Answer general knowledge and customer
            support questions clearly and helpfully.
            """
        ),
        ("human", state["question"])
    ])

    return {
        "specialist_response": response.content
    }


# =====================================
# 8. Supervisor Final Response
# =====================================

def supervisor_finalize(state: AgentState):

    response = llm.invoke([
        (
            "system",
            """
            You are the Supervisor.

            Review the response from the specialized agent.
            Produce a clear, helpful final answer.
            Do not invent information or claim actions
            that have not been performed.
            """
        ),
        (
            "human",
            f"""
            User Question:
            {state['question']}

            Selected Agent:
            {state['category']}

            Specialist Response:
            {state['specialist_response']}
            """
        )
    ])

    return {
        "final_answer": response.content
    }


# =====================================
# 9. Conditional Routing
# =====================================

def route_agent(state: AgentState):

    return state["category"]


# =====================================
# 10. Build LangGraph
# =====================================

workflow = StateGraph(AgentState)

# Register nodes
workflow.add_node("supervisor", supervisor)

workflow.add_node("technical", technical_agent)
workflow.add_node("billing", billing_agent)
workflow.add_node("general", general_agent)

workflow.add_node("finalize", supervisor_finalize)


# Define execution flow
workflow.add_edge(START, "supervisor")


# Supervisor selects specialized agent
workflow.add_conditional_edges(
    "supervisor",
    route_agent,
    {
        "technical": "technical",
        "billing": "billing",
        "general": "general"
    }
)


# Workers return to supervisor finalization
workflow.add_edge("technical", "finalize")
workflow.add_edge("billing", "finalize")
workflow.add_edge("general", "finalize")

workflow.add_edge("finalize", END)


# Compile graph
app = workflow.compile()


# =====================================
# 11. Rich Result Display
# =====================================

def display_result(question, result):

    table = Table(
        title="SUPERVISOR MULTI-AGENT SYSTEM",
        box=box.ROUNDED,
        show_lines=True,
        expand=True
    )

    table.add_column("Field", style="cyan")
    table.add_column("Execution Result", style="white")

    table.add_row("User Query", question)

    table.add_row(
        "Supervisor Decision",
        result["category"].upper()
    )

    table.add_row(
        "Selected Agent",
        result["category"].capitalize() + " Agent"
    )

    table.add_row(
        "Specialist Response",
        result["specialist_response"]
    )

    table.add_row(
        "Final Supervisor Response",
        result["final_answer"]
    )

    console.print()
    console.print(table)


# =====================================
# 12. Main Application
# =====================================

def main():

    console.print(
        Panel(
            "[bold cyan]LangGraph Supervisor Multi-Agent System[/bold cyan]\n"
            "Technical | Billing | General",
            border_style="blue"
        )
    )

    while True:

        question = console.input(
            "\n[bold yellow]Enter your question:[/bold yellow] "
        ).strip()

        if question.lower() in ["exit", "quit"]:
            console.print("[green]Application stopped.[/green]")
            break

        if not question:
            continue

        try:

            with console.status(
                "[bold cyan]Supervisor delegating task...[/bold cyan]"
            ):

                result = app.invoke({
                    "question": question,
                    "category": "",
                    "specialist_response": "",
                    "final_answer": ""
                })

            display_result(question, result)

        except Exception as error:

            console.print(
                Panel(
                    str(error),
                    title="Execution Error",
                    border_style="red"
                )
            )


if __name__ == "__main__":
    main()
