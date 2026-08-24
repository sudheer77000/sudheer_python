from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware, AgentMiddleware
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

#api_key = "YOUR_OPENAI_API_KEY"

@tool
def customer_lookup(query: str) -> str:
    """Look up customer information."""
    return f"Customer record found for query: {query}"


# -----------------------------------------
# Middleware to print processed message
# -----------------------------------------

class PrintProcessedInput(AgentMiddleware):

    def wrap_model_call(self, request, handler):

        print("\n========== AFTER PII MIDDLEWARE ==========")

        messages = request.state["messages"]

        for message in messages:
            print(f"{message.type}: {message.content}")

        print("==========================================\n")

        return handler(request)


# -----------------------------------------
# Create Agent
# -----------------------------------------

agent = create_agent(
    model=ChatOpenAI(
        model="gpt-4o",
        api_key=api_key,
        temperature=0
    ),

    tools=[customer_lookup],

    middleware=[

        # 1. NAME → HASH
        PIIMiddleware(
            "ip",
            strategy="hash",
            apply_to_input=True,
        ),

        # 2. EMAIL → REDACT
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
        ),

        # 3. CREDIT CARD → MASK
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
        ),

        # 4. API KEY → BLOCK
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
            apply_to_input=True,
        ),

        # Print the processed message
        PrintProcessedInput(),
    ],
)


# -----------------------------------------
# User Input
# -----------------------------------------

print("==========================================")
print("       PII Middleware Demo")
print("==========================================")
print("Strategies:")
print("  IP          → HASH")
print("  Email       → REDACT")
print("  Credit Card → MASK")
print("  API Key     → BLOCK")
print("\nType 'exit' to quit.")


while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Exiting...")
        break

    try:

        response = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        })

        print("\nAgent:", response["messages"][-1].content)

    except Exception as e:

        print("\n❌ REQUEST BLOCKED")
        print("Reason:", e)