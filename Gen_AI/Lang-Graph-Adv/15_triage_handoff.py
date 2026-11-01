
from typing import TypedDict, Literal, Annotated
from uuid import uuid4

from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()


# ------------------------------------------
# 1. Configuration
# ------------------------------------------

console = Console()

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

MAX_CLARIFICATIONS = 3


# ------------------------------------------
# 2. Triage structured output
# ------------------------------------------

class TriageDecision(BaseModel):

    status: Literal[
        "need_more_info",
        "ready",
        "human"
    ]

    category: Literal[
        "technical",
        "billing",
        "general",
        "human"
    ]

    priority: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ]

    reason: str

    follow_up_question: str = Field(
        default="",
        description=(
            "Ask one specific question if essential "
            "information is missing. Otherwise empty."
        )
    )


triage_llm = llm.with_structured_output(TriageDecision)


# ------------------------------------------
# 3. LangGraph state
# ------------------------------------------

class AgentState(TypedDict):

    # add_messages preserves existing conversation history
    messages: Annotated[list[AnyMessage], add_messages]

    category: str
    priority: str
    reason: str
    status: str
    follow_up_question: str
    clarification_count: int
    answer: str


# ------------------------------------------
# 4. Triage node
# ------------------------------------------

def triage_node(state: AgentState):

    history = "\n".join(
        f"{message.type}: {message.content}"
        for message in state["messages"]
    )

    prompt = f"""
You are a professional conversational customer support
triage agent.

Your responsibility is to understand the user's problem
before routing it to a specialist.

Conversation:
{history}

Clarification questions already asked:
{state['clarification_count']}

Rules:

1. Understand the user's actual problem.
2. Identify only essential missing information.
3. Ask ONE focused follow-up question at a time.
4. Never repeat a question already answered.
5. Do not ask unnecessary questions.
6. If you have enough information, set status to ready.
7. If human intervention is necessary, set status to human.
8. Do not invent information.

Categories:
- technical: API, software, bugs, login, system errors.
- billing: payments, invoices, refunds, subscriptions.
- general: FAQs and general product questions.
- human: cases requiring human intervention.

Priorities:
- low: ordinary informational request.
- medium: normal support issue.
- high: significant disruption.
- critical: severe outage, suspected fraud or security incident.

If information is missing:
- status = need_more_info
- provide one follow_up_question

If enough information is available:
- status = ready
- follow_up_question = empty string

If human intervention is necessary:
- status = human
- category = human
"""

    decision = triage_llm.invoke(prompt)

    # Stop endless clarification loops
    if (
        decision.status == "need_more_info"
        and state["clarification_count"] >= MAX_CLARIFICATIONS
    ):
        return {
            "status": "human",
            "category": "human",
            "priority": decision.priority,
            "reason": (
                "Maximum clarification attempts reached. "
                + decision.reason
            ),
            "follow_up_question": ""
        }

    return {
        "status": decision.status,
        "category": decision.category,
        "priority": decision.priority,
        "reason": decision.reason,
        "follow_up_question": decision.follow_up_question
    }


# ------------------------------------------
# 5. Clarification node
# ------------------------------------------

def clarification_node(state: AgentState):

    question = state["follow_up_question"]

    # Pause graph and wait for user input
    user_answer = interrupt({
        "question": question
    })

    # Append answer without deleting conversation history
    return {
        "messages": [
            HumanMessage(content=user_answer)
        ],
        "clarification_count": (
            state["clarification_count"] + 1
        )
    }


# ------------------------------------------
# 6. Specialist agents
# ------------------------------------------

def technical_agent(state: AgentState):

    response = llm.invoke([
        (
            "system",
            "You are a technical support specialist. "
            "Use the complete conversation to resolve "
            "the customer's technical issue."
        ),
        *state["messages"]
    ])

    return {"answer": response.content}


def billing_agent(state: AgentState):

    response = llm.invoke([
        (
            "system",
            "You are a billing support specialist. "
            "Use the complete conversation to help the customer. "
            "Never claim a payment or refund action was completed "
            "unless it was actually verified."
        ),
        *state["messages"]
    ])

    return {"answer": response.content}


def general_agent(state: AgentState):

    response = llm.invoke([
        (
            "system",
            "You are a general customer support specialist. "
            "Answer using the complete conversation."
        ),
        *state["messages"]
    ])

    return {"answer": response.content}


def human_agent(state: AgentState):

    return {
        "answer": (
            "This request requires human support. "
            "The clarification limit may have been reached, "
            "or the issue requires human intervention. "
            "Please contact the support team."
        )
    }


# ------------------------------------------
# 7. Conditional routing
# ------------------------------------------

def choose_next_step(state: AgentState):

    if state["status"] == "need_more_info":
        return "clarify"

    if state["status"] == "human":
        return "human"

    return state["category"]


# ------------------------------------------
# 8. Build LangGraph
# ------------------------------------------

builder = StateGraph(AgentState)

builder.add_node("triage", triage_node)
builder.add_node("clarify", clarification_node)

builder.add_node("technical", technical_agent)
builder.add_node("billing", billing_agent)
builder.add_node("general", general_agent)
builder.add_node("human", human_agent)

builder.add_edge(START, "triage")

builder.add_conditional_edges(
    "triage",
    choose_next_step,
    {
        "clarify": "clarify",
        "technical": "technical",
        "billing": "billing",
        "general": "general",
        "human": "human"
    }
)

# After user answers, run triage again
builder.add_edge("clarify", "triage")

for node in ["technical", "billing", "general", "human"]:
    builder.add_edge(node, END)


# ------------------------------------------
# 9. Compile with persistence
# ------------------------------------------

checkpointer = InMemorySaver()

app = builder.compile(
    checkpointer=checkpointer
)


# ------------------------------------------
# 10. Display final result
# ------------------------------------------

def display_result(result):

    table = Table(
        title="Final Triage Analysis",
        show_lines=True
    )

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")

    table.add_row("Category", result["category"].upper())
    table.add_row("Priority", result["priority"].upper())
    table.add_row("Reason", result["reason"])
    table.add_row(
        "Clarification Questions",
        str(result["clarification_count"])
    )

    console.print(table)

    console.print(
        Panel(
            result["answer"],
            title="Specialist Response",
            border_style="green"
        )
    )


# ------------------------------------------
# 11. Interactive execution
# ------------------------------------------

def run_triage():

    # Unique conversation ID
    config = {
        "configurable": {
            "thread_id": str(uuid4())
        }
    }

    question = console.input(
        "\n[bold cyan]User: [/bold cyan]"
    )

    if not question.strip():
        return

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ],
            "category": "",
            "priority": "",
            "reason": "",
            "status": "",
            "follow_up_question": "",
            "clarification_count": 0,
            "answer": ""
        },
        config=config
    )

    # Continue until graph reaches END
    while result.get("__interrupt__"):

        interrupt_data = result["__interrupt__"][0].value

        console.print(
            Panel(
                interrupt_data["question"],
                title="Triage Agent - Follow-up Question",
                border_style="yellow"
            )
        )

        user_answer = console.input(
            "[bold cyan]User: [/bold cyan]"
        )

        result = app.invoke(
            Command(resume=user_answer),
            config=config
        )

    display_result(result)


# ------------------------------------------
# 12. Main
# ------------------------------------------

console.print(
    Panel(
        "[bold cyan]Conversational Triage Agent[/bold cyan]\n"
        "Maximum clarification questions: 3",
        border_style="cyan"
    )
)

while True:

    command = console.input(
        "\n[bold yellow]Press ENTER to start a conversation "
        "or type exit: [/bold yellow]"
    )

    if command.lower().strip() in ["exit", "quit"]:
        break

    try:
        run_triage()

    except Exception as error:
        console.print(
            f"[bold red]Error: {error}[/bold red]"
        )

console.print("[green]Application closed.[green]")
