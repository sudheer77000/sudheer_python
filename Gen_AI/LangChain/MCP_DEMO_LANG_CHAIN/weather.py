from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Weather",port=8001)

@mcp.tool()
async def get_weather(location:str) -> str:
    """Get the Weather Location."""
    return "it's been raining in " + location

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )