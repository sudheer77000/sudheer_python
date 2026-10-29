
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.live import Live
from rich.spinner import Spinner

console = Console()

# User message
console.print(
    Panel("Explain artificial intelligence simply.",
          title="[bold cyan]You[/bold cyan]",
          border_style="cyan")
)

# AI thinking animation
console.print()
console.print("[yellow]AI is thinking...[/yellow]")

with Live(
    Spinner("dots", text=" Analyzing your question..."),
    console=console,
    refresh_per_second=10,
) as live:
    for i in range(20):
        time.sleep(0.1)

console.print("[green]✓ Thinking complete![/green]\n")

# AI progress bar
with Progress(
    TextColumn("[bold blue]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeElapsedColumn(),
    console=console,
) as progress:
    task = progress.add_task("Generating response", total=100)

    while not progress.finished:
        progress.update(task, advance=5)
        time.sleep(0.05)

# AI response
answer = (
    "Artificial intelligence (AI) allows computers to perform "
    "tasks such as understanding language, answering questions, "
    "and solving problems."
)

console.print(
    Panel(answer, title="[bold green]ChatGPT[/bold green]",
          border_style="green")
)
