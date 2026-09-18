from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print("########## Addition Tool Invoked #############")
    return a + b

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    print("########## Weather Tool Invoked #############")
    return f"Weather in {city} is sunny"

# 2. OpenAI model
llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0
)


agent = create_agent(llm, [add, get_weather])
print(agent)


Question = input("User Question : ")

response = agent.invoke({
    "messages": [("user", Question)]
})

print(response["messages"][-1].content)