from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    print(f"\n>>> TOOL CALLED: get_weather(city='{city}')")
    return f"The weather in {city} is 32°C."


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    print(f"\n>>> TOOL CALLED: calculate(expression='{expression}')")

    try:
        return str(eval(expression))
    except Exception:
        return "Invalid mathematical expression."


@tool
def get_exchange_rate(currency: str) -> str:
    """Get the exchange rate for a currency against USD."""
    print(f"\n>>> TOOL CALLED: get_exchange_rate(currency='{currency}')")

    rates = {
        "EUR": "1 EUR = 1.17 USD",
        "GBP": "1 GBP = 1.35 USD",
        "INR": "1 INR = 0.012 USD",
        "AED": "1 AED = 0.272 USD"
    }

    return rates.get(
        currency.upper(),
        "Exchange rate not available."
    )


model = ChatGroq(
    model="qwen/qwen3.6-27b",
    temperature=0
)


agent = create_agent(
    model=model,
    tools=[
        get_weather,
        calculate,
        get_exchange_rate
    ],
    system_prompt="""
You are an agent with access to weather, calculation,
and currency exchange tools.

Use a tool when the user's question is related to one
of these capabilities.

If the question is NOT related to any available tool,
respond exactly:

Info Not Found

Do not try to answer unrelated questions from your
general knowledge.
"""
)


user_input = input("\nEnter your question: ")

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": user_input
        }
    ]
})

print("\n>>> FINAL ANSWER:")
print(result["messages"][-1].content)

print(result)