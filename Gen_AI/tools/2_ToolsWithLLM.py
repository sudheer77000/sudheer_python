from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"Weather in {city} is sunny"

# 2. OpenAI model
llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0
)

llm_with_tools = llm.bind_tools([add, get_weather])
print(llm_with_tools)

Question = input("User Question : ")

response = llm_with_tools.invoke(
    Question
)
print(response)
print("#" * 100)
print(response.content)
print("#" * 100)
print(response.tool_calls)

# 1. Map your tools
tools_map = {
    "get_weather": get_weather,
    "add": add
}

#response = llm_with_tools.invoke("What is the weather in Goa?")

if response.tool_calls:
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        # Look up the tool and invoke it properly
        selected_tool = tools_map[tool_name]
        result = selected_tool.invoke(tool_args)
        
        print(f"Tool Result: {result}")

# result = add.invoke({"a": 10, "b": 20})
# result1 = get_weather.invoke({"city":"New Delhi"})

# print(result)
# print(result1)