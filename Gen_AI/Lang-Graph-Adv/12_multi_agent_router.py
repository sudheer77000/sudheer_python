
import time
from typing import TypedDict, Literal

from pydantic import BaseModel
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import box

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from openai import OpenAI

from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()



# Initialize Rich console
console = Console()

# Initialize OpenAI
router_llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

client = OpenAI()


# 1. Routing schema
class Route(BaseModel):
    category: Literal[
        "cricket",
        "movies",
        "politics",
        "general"
    ]


# 2. Shared state
class AgentState(TypedDict):
    question: str
    category: str
    answer: str
    sources: list


# 3. Router
structured_router = router_llm.with_structured_output(Route)

def router(state: AgentState):

    result = structured_router.invoke(f"""
    Classify the question into one category:

    cricket: Cricket matches, players, scores and news.
    movies: Movies, actors, reviews and entertainment.
    politics: Elections, governments and political news.
    general: Everything else.

    Question: {state['question']}
    """)

    return {"category": result.category}


# 4. Common OpenAI Web Search
def search_agent(question, role):

    response = client.responses.create(
        model="gpt-4.1-mini",

        instructions=f"""
        You are a specialized {role} AI agent.

        Always use web search to answer.
        Prefer reliable and recent sources.
        Provide a clear summary.
        Include citations and source references.
        If information is unavailable, say so.
        """,

        tools=[
            {
                "type": "web_search",
                "search_context_size": "medium"
            }
        ],

        tool_choice="required",
        input=question
    )

    # Extract cited URLs
    sources = []

    for item in response.output:
        if item.type == "message":
            for content in item.content:
                for annotation in getattr(
                    content, "annotations", []
                ) or []:

                    if annotation.type == "url_citation":
                        url = getattr(annotation, "url", None)
                        title = getattr(annotation, "title", None)

                        if url and url not in [
                            s["url"] for s in sources
                        ]:
                            sources.append({
                                "title": title or "Source",
                                "url": url
                            })

    return response.output_text, sources


# 5. Specialized agents

def cricket_agent(state: AgentState):

    answer, sources = search_agent(
        state["question"],
        "Cricket News and Analysis"
    )

    return {
        "answer": answer,
        "sources": sources
    }


def movies_agent(state: AgentState):

    answer, sources = search_agent(
        state["question"],
        "Movies and Entertainment"
    )

    return {
        "answer": answer,
        "sources": sources
    }


def politics_agent(state: AgentState):

    answer, sources = search_agent(
        state["question"],
        "Political News and Analysis"
    )

    return {
        "answer": answer,
        "sources": sources
    }


def general_agent(state: AgentState):

    answer, sources = search_agent(
        state["question"],
        "General Knowledge and Research"
    )

    return {
        "answer": answer,
        "sources": sources
    }


# 6. Conditional routing
def route_to_agent(state: AgentState):
    return state["category"]


# 7. Build LangGraph
workflow = StateGraph(AgentState)

workflow.add_node("router", router)

workflow.add_node("cricket", cricket_agent)
workflow.add_node("movies", movies_agent)
workflow.add_node("politics", politics_agent)
workflow.add_node("general", general_agent)

workflow.add_edge(START, "router")

workflow.add_conditional_edges(
    "router",
    route_to_agent,
    {
        "cricket": "cricket",
        "movies": "movies",
        "politics": "politics",
        "general": "general"
    }
)

workflow.add_edge("cricket", END)
workflow.add_edge("movies", END)
workflow.add_edge("politics", END)
workflow.add_edge("general", END)

app = workflow.compile()


# 8. Rich output table
def display_result(question, result, elapsed):

    category = result["category"]

    agents = {
        "cricket": "Cricket Agent",
        "movies": "Movies Agent",
        "politics": "Politics Agent",
        "general": "General Agent"
    }

    # Main results table
    table = Table(
        title="AI WEB SEARCH RESULTS",
        box=box.ROUNDED,
        show_lines=True,
        expand=True
    )

    table.add_column("Field", style="cyan", width=18)
    table.add_column("Result", style="white")

    table.add_row("Question", question)
    table.add_row("Category", category.upper())
    table.add_row("Selected Agent", agents[category])
    table.add_row("Web Search", "[green]Executed[/green]")
    table.add_row("Execution Time", f"{elapsed:.2f} seconds")

    table.add_row(
        "AI Answer",
        Markdown(result["answer"])
    )

    console.print()
    console.print(table)

    # Sources table
    sources = result.get("sources", [])

    if sources:
        source_table = Table(
            title="WEB SEARCH SOURCES",
            box=box.SIMPLE,
            expand=True
        )

        source_table.add_column("#", style="cyan")
        source_table.add_column("Title", style="white")
        source_table.add_column("URL", style="blue")

        for index, source in enumerate(sources, 1):
            source_table.add_row(
                str(index),
                source["title"],
                source["url"]
            )

        console.print(source_table)


# 9. Run application
def main():

    console.print(
        Panel(
            "[bold cyan]LangGraph Multi-Agent Web Search[/bold cyan]\n"
            "Cricket | Movies | Politics | General",
            border_style="blue"
        )
    )

    while True:

        question = console.input(
            "\n[bold yellow]Ask your question[/bold yellow] "
        ).strip()

        if question.lower() in ["exit", "quit"]:
            console.print("[bold green]Goodbye![/bold green]")
            break

        if not question:
            continue

        start_time = time.perf_counter()

        try:
            with console.status(
                "[bold cyan]Routing and searching the web...[/bold cyan]"
            ):

                result = app.invoke({
                    "question": question,
                    "category": "",
                    "answer": "",
                    "sources": []
                })

            elapsed = time.perf_counter() - start_time

            display_result(question, result, elapsed)

        except Exception as error:
            console.print(
                Panel(
                    str(error),
                    title="Application Error",
                    border_style="red"
                )
            )


if __name__ == "__main__":
    main()
