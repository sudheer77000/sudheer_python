
import os
import re
import time

import openai
from openai import OpenAI
from dotenv import load_dotenv

from rich.console import Console, Group
from rich.panel import Panel
from rich.live import Live
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    SpinnerColumn,
)

load_dotenv()

console = Console()


def create_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        console.print("[red]OPENAI_API_KEY not found in .env[/red]")
        return None

    return OpenAI(
        api_key=api_key,
        timeout=60.0,
        max_retries=0,
    )


def ask_ai(client, question):
    console.print(
        Panel(question, title="You", border_style="cyan")
    )

    answer = ""
    pending = ""

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
        console=console,
        auto_refresh=False,
    )

    task = progress.add_task("Thinking...", total=100)

    # Show the thinking indicator and progress bar.
    with Live(
        Group(
            Panel("Thinking...", title="ChatGPT",
                  border_style="green"),
            progress,
        ),
        console=console,
        refresh_per_second=20,
    ) as live:

        try:
            stream = client.responses.create(
                model="gpt-5",
                input=question,
                stream=True,
            )

            progress.update(
                task, description="Receiving response"
            )

            for event in stream:
                if event.type == "response.output_text.delta":
                    pending += event.delta

                    # Display complete words as they arrive.
                    words = re.findall(r"\S+\s*", pending)

                    if pending and not pending[-1].isspace():
                        ready_words = words[:-1]
                        pending = words[-1] if words else pending
                    else:
                        ready_words = words
                        pending = ""

                    for word in ready_words:
                        answer += word

                        # Estimated progress, not model progress.
                        percent = min(
                            95,
                            len(answer) / (len(answer) + 250) * 100,
                        )
                        progress.update(
                            task,
                            completed=percent,
                        )

                        live.update(
                            Group(
                                Panel(
                                    answer + "▌",
                                    title="ChatGPT is typing...",
                                    border_style="green",
                                ),
                                progress,
                            )
                        )

                        time.sleep(0.025)

                elif event.type == "response.completed":
                    break

                elif event.type == "response.failed":
                    raise RuntimeError(
                        "The AI response failed."
                    )

            # Display any final word that was buffered.
            if pending:
                answer += pending

            progress.update(
                task,
                completed=100,
                description="Response complete",
            )

            live.update(
                Group(
                    Panel(
                        answer or "No text response received.",
                        title="ChatGPT",
                        border_style="green",
                    ),
                    progress,
                )
            )

        except openai.APITimeoutError:
            live.update(
                Panel(
                    "Request timed out. Please try again.",
                    title="Timeout",
                    border_style="red",
                )
            )

        except openai.APIConnectionError:
            live.update(
                Panel(
                    "Could not connect to OpenAI. "
                    "Check your internet connection.",
                    title="Connection error",
                    border_style="red",
                )
            )

        except openai.APIStatusError as error:
            live.update(
                Panel(
                    f"API error {error.status_code}: "
                    f"{error.message}",
                    title="API error",
                    border_style="red",
                )
            )

        except KeyboardInterrupt:
            live.update(
                Panel(
                    "Response interrupted.",
                    title="Cancelled",
                    border_style="yellow",
                )
            )

        except (openai.APIError, RuntimeError) as error:
            live.update(
                Panel(
                    str(error),
                    title="Error",
                    border_style="red",
                )
            )

    console.print()


def main():
    client = create_client()

    if client is None:
        return

    console.print(
        Panel(
            "Ask me anything!\nType 'exit' to quit.",
            title="Python AI Chat",
            border_style="blue",
        )
    )

    try:
        while True:
            question = console.input(
                "\n[bold cyan]You:[/bold cyan] "
            ).strip()

            if question.lower() in {"exit", "quit"}:
                console.print("[yellow]Goodbye![/yellow]")
                break

            if question:
                ask_ai(client, question)

    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]Chat closed.[/yellow]")

    finally:
        client.close()


if __name__ == "__main__":
    main()
