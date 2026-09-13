from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

import asyncio
import sys
import os

load_dotenv()


async def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    math_server = os.path.join(base_dir, "maths_server.py")

    # Initialize directly without 'async with'
    client = MultiServerMCPClient(
        {
            "math": {
                "command": sys.executable,
                "args": [math_server],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8001/mcp",
                "transport": "streamable-http",
            },
        }
    )
    
    tools = await client.get_tools()

    print("MCP Tools:")
    for tool in tools:
        print(tool.name)

    model = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

    agent = create_agent(
        model,
        tools=tools,
        system_prompt="You are a helpful assistant that can use tools to answer math and weather questions."
    )

    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
 #                   "content": "what's (3 + 3) * 12?"
                    "content": "what weather in Dubai?"
                }
            ]
        }
    )

    print("\nResponse:")
    print(response["messages"][-1].content)


asyncio.run(main())