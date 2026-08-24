from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain_core.tools import tool
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# =========================================================
# Tools
# =========================================================

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    return f"Email sent to {to} with subject: {subject}"


@tool
def delete_records(table: str, condition: str) -> str:
    """Delete records from the database."""
    return f"Deleted records from {table} where {condition}"


# =========================================================
# Create HITL Agent
# =========================================================

hitl_agent = create_agent(
    model="gpt-4o",
    tools=[
        search_web,
        send_email,
        delete_records
    ],

    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": True,       # Human approval required
                "delete_records": True,   # Human approval required
                "search_web": False,      # Automatically approved
            }
        ),
    ],

    # Required for HITL state persistence
    checkpointer=InMemorySaver(),
)


# =========================================================
# Configuration
# =========================================================

config = {
    "configurable": {
        "thread_id": "user-1"
    }
}


# =========================================================
# User Input
# =========================================================

print("==========================================")
print("       Human-in-the-Loop Agent")
print("==========================================")
print()
print("Examples:")
print("  Search for latest AI news")
print("  Send an email to john@example.com")
print("  Delete records from customers where id=10")
print()
print("Type 'exit' to quit.")
print()


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Exiting...")
        break

    try:

        # -------------------------------------------------
        # First agent execution
        # -------------------------------------------------

        result = hitl_agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            },
            config=config
        )

        # -------------------------------------------------
        # Check if agent is waiting for human approval
        # -------------------------------------------------

        if "__interrupt__" in result:

            print("\n⚠️ HUMAN APPROVAL REQUIRED")
            print("------------------------------------------")

            interrupts = result["__interrupt__"]

            for interrupt in interrupts:
                print(interrupt)

            print("------------------------------------------")

            approval = input(
                "\nApprove this action? (yes/no): "
            ).strip().lower()

            # -------------------------------------------------
            # Human decision
            # -------------------------------------------------

            if approval in ["yes", "y"]:

                print("\n✅ Action approved")

                result = hitl_agent.invoke(
                    Command(
                        resume={
                            "decisions": [
                                {
                                    "type": "approve"
                                }
                            ]
                        }
                    ),
                    config=config
                )

            else:

                print("\n❌ Action rejected")

                result = hitl_agent.invoke(
                    Command(
                        resume={
                            "decisions": [
                                {
                                    "type": "reject",
                                    "message": "Human rejected the action."
                                }
                            ]
                        }
                    ),
                    config=config
                )

        # -------------------------------------------------
        # Print final response
        # -------------------------------------------------

        messages = result.get("messages", [])

        if messages:
            print("\nAgent:", messages[-1].content)

    except Exception as e:

        print("\n❌ ERROR")
        print(e)

    print()