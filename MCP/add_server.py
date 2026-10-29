from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("CalculatorServer")

# Define one tool
@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

# Start the server using stdio transport
if __name__ == "__main__":
    mcp.run(transport="stdio")
