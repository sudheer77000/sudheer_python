
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Read numbers from the user
    try:
        a = int(input("Enter the first number: "))
        b = int(input("Enter the second number: "))
    except ValueError:
        print("Invalid input! Please enter integers.")
        return

    # Configure the MCP server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("add_server.py"))],
    )

    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize the session
            await session.initialize()

            # Call the addition tool
            result = await session.call_tool(
                "add_numbers",
                arguments={"a": a, "b": b}
            )

            # Display the result
            print("\nResult:")
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
