import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["maths_server.py"],
    )

    print("Starting MCP server...")

    async with stdio_client(server_params) as (read, write):

        print("Creating MCP session...")

        async with ClientSession(read, write) as session:

            print("Initializing MCP...")

            await session.initialize()

            print("MCP initialized successfully!")

            tools = await session.list_tools()

            print("\nAvailable tools:")

            for tool in tools.tools:
                print("-", tool.name)

            print("\nCalling add(3, 3)...")

            result = await session.call_tool(
                "add",
                {"a": 3, "b": 3}
            )

            print("Result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())