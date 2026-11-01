
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()


console = Console()


# --------------------------------
# 1. Define Mathematical Tools
# --------------------------------

@tool
def addition(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@tool
def subtraction(a: float, b: float) -> float:
    """Subtract second number from first number."""
    return a - b


@tool
def multiplication(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def division(a: float, b: float) -> float:
    """Divide first number by second number."""
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b


# --------------------------------
# 2. Register Tools
# --------------------------------

tools = [
    addition,
    subtraction,
    multiplication,
    division
]


# --------------------------------
# 3. Initialize OpenAI Model
# --------------------------------

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# --------------------------------
# 4. Create ReAct Agent
# --------------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
    You are a mathematical assistant.

    Use the appropriate tool for every calculation:
    - addition
    - subtraction
    - multiplication
    - division

    Never guess calculation results.
    Explain the final answer clearly.
    """
)


# --------------------------------
# 5. Display Results Using Rich
# --------------------------------

def display_result(question, result):

    messages = result["messages"]

    table = Table(
        title="ReAct Mathematical Agent",
        box=box.ROUNDED,
        show_lines=True
    )

    table.add_column("Step", style="cyan")
    table.add_column("Agent Execution", style="white")

    table.add_row("User Input", question)

    step = 1

    for message in messages[1:]:

        if message.type == "ai":

            if message.tool_calls:
                for call in message.tool_calls:
                    table.add_row(
                        f"Step {step}",
                        f"Tool Selected: {call['name']}\n"
                        f"Arguments: {call['args']}"
                    )
                    step += 1

        elif message.type == "tool":

            table.add_row(
                f"Step {step}",
                f"Tool Result: {message.content}"
            )
            step += 1

    final_answer = messages[-1].content

    table.add_row("Final Answer", final_answer)

    console.print()
    console.print(table)


# --------------------------------
# 6. Run Application
# --------------------------------

def main():

    console.print(
        Panel(
            "[bold cyan]LangGraph ReAct Math Agent[/bold cyan]\n"
            "Addition | Subtraction | Multiplication | Division",
            border_style="blue"
        )
    )

    while True:

        question = console.input(
            "\n[bold yellow]Enter calculation:[/bold yellow] "
        )

        if question.lower() in ["exit", "quit"]:
            console.print("[green]Goodbye![/green]")
            break

        try:

            with console.status(
                "[bold cyan]Agent is thinking and executing tools...[/bold cyan]"
            ):

                result = agent.invoke({
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                })

            display_result(question, result)

        except Exception as error:

            console.print(
                Panel(
                    str(error),
                    title="Error",
                    border_style="red"
                )
            )


if __name__ == "__main__":
    main()
