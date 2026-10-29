
from mcp.server.fastmcp import FastMCP

server = FastMCP("Simple Calculator Server")


# 1. RESOURCE: Provides information
@server.resource("calculator://info")
def calculator_info() -> str:
    """Provide information about the calculator."""
    return "This calculator can add two numbers."


# 2. TOOL: Performs an operation
@server.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b


# 3. PROMPT: Provides a reusable instruction
@server.prompt()
def explain_addition(a: int, b: int) -> str:
    """Generate an instruction to explain an addition."""
    return f"Explain step by step how to calculate {a} + {b}."


if __name__ == "__main__":
    server.run(transport="stdio")
