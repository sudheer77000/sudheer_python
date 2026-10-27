
import os
import sys

from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain.tools import tool

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.status import Status
from rich.theme import Theme
from rich.traceback import install

# -----------------------------
# Rich terminal setup
# -----------------------------
theme = Theme({
    "info": "cyan",
    "success": "green",
    "warning": "yellow",
    "error": "bold red",
})

console = Console(theme=theme)
install(show_locals=False)

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    console.print(
        "[error]OPENAI_API_KEY not found.[/error]\n"
        "Check that your .env file is in the project directory."
    )
    sys.exit(1)


# -----------------------------
# Custom tool
# -----------------------------
@tool
def get_company_info(company: str) -> str:
    """Return sample information about a company by name."""
    sample_data = {
        "openai": "AI research and product company.",
        "google": "Technology company known for search and cloud services.",
        "microsoft": "Technology company known for software and cloud services.",
    }

    return sample_data.get(
        company.lower().strip(),
        f"No sample information available for {company}."
    )


# -----------------------------
# Create Deep Agent
# -----------------------------
console.print(
    Panel.fit(
        "[bold cyan]LangChain Deep Agent[/bold cyan]\n"
        "[dim]Powered by OpenAI + DeepAgents + Rich[/dim]",
        border_style="cyan",
    )
)

with console.status(
    "[bold cyan]Initializing Deep Agent...[/bold cyan]",
    spinner="dots",
):
    agent = create_deep_agent(
        model="openai:gpt-4.1",
        tools=[get_company_info],
        system_prompt="""
You are a research assistant.

For complex requests:
1. Plan the work.
2. Break the task into smaller steps.
3. Use available tools when appropriate.
4. Organize findings and verify available information.
5. Clearly distinguish sample data from verified facts.
6. Return a clear, well-structured answer.

Do not claim to have performed live research unless
you have access to a suitable research tool.
""",
    )

console.print("[success]Agent initialized successfully![/success]\n")


# -----------------------------
# Interactive chat loop
# -----------------------------
def main():
    """Run an interactive terminal chat with the Deep Agent."""

    messages = []

    console.print(
        Panel(
            "Ask questions or give the agent a task.\n"
            "Type [bold]exit[/bold] or [bold]quit[/bold] to stop.",
            title="Instructions",
            border_style="green",
        )
    )

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]You[/bold green]")

            if user_input.strip().lower() in {"exit", "quit"}:
                console.print(
                    Panel("Goodbye!", border_style="yellow")
                )
                break

            if not user_input.strip():
                continue

            messages.append({
                "role": "user",
                "content": user_input,
            })

            with console.status(
                "[bold cyan]Agent is thinking and using tools...[/bold cyan]",
                spinner="dots",
            ):
                result = agent.invoke({"messages": messages})

            # Keep returned conversation state for follow-up turns
            messages = result["messages"]

            final_message = messages[-1].content

            if isinstance(final_message, str):
                answer = final_message
            else:
                answer = str(final_message)

            console.print(
                Panel(
                    Markdown(answer),
                    title="[bold cyan]Deep Agent[/bold cyan]",
                    border_style="cyan",
                    padding=(1, 2),
                )
            )

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user.[/yellow]")
            break

        except Exception as exc:
            console.print(
                Panel(
                    f"{type(exc).__name__}: {exc}",
                    title="[error]Agent Error[/error]",
                    border_style="red",
                )
            )


if __name__ == "__main__":
    main()
