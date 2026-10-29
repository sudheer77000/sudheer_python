from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="AI Model Results")

table.add_column("Model", style="cyan")
table.add_column("Accuracy", style="green")
table.add_column("Status", style="yellow")

table.add_row("Model A", "95%", "Ready")
table.add_row("Model B", "92%", "Training")

console.print(table)