
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Find server.py in the same folder
    server_path = Path(__file__).parent / "cal_server.py"

    # Configure the server process
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )

    # Connect to the server
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as client:

            await client.initialize()

            print("\n=== MCP CONNECTED ===")

            # 1. READ RESOURCE
            print("\n1. RESOURCE")

            resource = await client.read_resource(
                "calculator://info"
            )

            for content in resource.contents:
                if hasattr(content, "text"):
                    print(content.text)

            # 2. CALL TOOL
            print("\n2. TOOL: ADD")

            result = await client.call_tool(
                "add",
                arguments={"a": 10, "b": 20},
            )

            for content in result.content:
                if hasattr(content, "text"):
                    print("Result:", content.text)

            # 3. GET PROMPT
            print("\n3. PROMPT")

            prompt = await client.get_prompt(
                "explain_addition",
                arguments={"a": "10", "b": "20"},
            )

            for message in prompt.messages:
                if hasattr(message.content, "text"):
                    print(message.content.text)


if __name__ == "__main__":
    asyncio.run(main())
