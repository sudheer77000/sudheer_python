
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("resource_server.py"))],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            # Discover available resources
            resources = await session.list_resources()

            print("Available resources:")
            for resource in resources.resources:
                print(resource.uri)

            # Read the live system metrics
            result = await session.read_resource(
                "system://metrics"
            )

            print("\nCurrent system metrics:")
            for item in result.contents:
                if hasattr(item, "text"):
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
