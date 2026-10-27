
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool

# Load API key from .env
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY not found. Check your .env file."
    )


# Define a custom tool
@tool
def get_weather(city: str) -> str:
    """Get sample weather information for a given city."""
    # Demo implementation; this is not live weather data.
    return f"Sample weather report for {city}: Sunny, 30°C."


# Create the normal agent
agent = create_agent(
    model="openai:gpt-4.1",
    tools=[get_weather],
    system_prompt=(
        "You are a helpful assistant. "
        "Use the get_weather tool when users ask about weather. "
        "Clearly identify sample data as simulated."
    ),
)


# Run the agent
if __name__ == "__main__":
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in Abu Dhabi?"
                }
            ]
        }
    )

    # Print the final response
    print("\nAgent response:")
    print(response["messages"][-1].content)
