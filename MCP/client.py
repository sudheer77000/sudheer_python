
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent, TextResourceContents

# Windows consoles default to cp1252, which cannot print characters like ₹ or °
sys.stdout.reconfigure(encoding="utf-8")


async def main():
    # Locate the MCP server script
    server_path = Path(__file__).parent / "server.py"

    # Configure the server process
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )

    print("Starting MCP client...")

    # Start the server and establish stdio communication
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as client:

            # Initialize the MCP session
            init_result = await client.initialize()

            print("=" * 60)
            print("CONNECTED TO MCP SERVER")
            print("=" * 60)

            print("\nProtocol Version:")
            print(init_result.protocolVersion)

            print("\n" + "=" * 60)
            print("TOOLS")
            print("=" * 60)

            tools_result = await client.list_tools()

            for tool in tools_result.tools:
                print("-", tool.name)

            print("\n" + "=" * 60)
            print("CALL TOOL: search_flights")
            print("=" * 60)

            tool_result = await client.call_tool(
                "search_flights",
                arguments={
                    "origin": "Bangalore",
                    "destination": "Dubai",
                },
            )

            for block in tool_result.content:
                if isinstance(block, TextContent):
                    print(block.text)

            print("\n" + "=" * 60)
            print("DIRECT RESOURCES")
            print("=" * 60)

            resources_result = await client.list_resources()

            for resource in resources_result.resources:
                print("-", resource.uri)

            print("\n" + "=" * 60)
            print("TRAVEL PREFERENCES")
            print("=" * 60)

            resource_result = await client.read_resource(
                "travel://preferences"
            )

            for content in resource_result.contents:
                if isinstance(content, TextResourceContents):
                    print(content.text)

            print("\n" + "=" * 60)
            print("RESOURCE TEMPLATES")
            print("=" * 60)

            templates_result = await client.list_resource_templates()

            for template in templates_result.resourceTemplates:
                print("-", template.uriTemplate)

            print("\n" + "=" * 60)
            print("WEATHER RESOURCE")
            print("=" * 60)

            weather_result = await client.read_resource(
                "weather://Dubai"
            )

            for content in weather_result.contents:
                if isinstance(content, TextResourceContents):
                    print(content.text)

            print("\n" + "=" * 60)
            print("PROMPTS")
            print("=" * 60)

            prompts_result = await client.list_prompts()

            for prompt in prompts_result.prompts:
                print("-", prompt.name)

            print("\n" + "=" * 60)
            print("VACATION PROMPT")
            print("=" * 60)

            prompt_result = await client.get_prompt(
                "plan_vacation",
                arguments={
                    "destination": "Dubai",
                    "days": "5",
                },
            )

            for message in prompt_result.messages:
                if isinstance(message.content, TextContent):
                    print(message.content.text)

            print("\n" + "=" * 60)
            print("MCP CLIENT COMPLETED SUCCESSFULLY")
            print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nClient stopped by user.")
    except Exception as exc:
        print(f"\nMCP client error: {exc}")
        raise