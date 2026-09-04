from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent


# ============================================================
# 1. CREATE TOOLS
# ============================================================

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print("ADD TOOL CALLED")
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    print("SUBTRACT TOOL CALLED")
    return a - b


# ============================================================
# 2. CREATE MODEL
# ============================================================

model = ChatOllama(
    model="qwen2.5:3b"
)


# ============================================================
# 3. CREATE REACT AGENT
# ============================================================

agent = create_react_agent(
    model=model,
    tools=[add, subtract]
)


# ============================================================
# 4. INVOKE AGENT
# ============================================================

result = agent.invoke({
    "messages": [
        ("user", "What is 20 + 10? and 40 - 9")
    ]
})


# ============================================================
# 5. PRINT MESSAGES
# ============================================================

for message in result["messages"]:
    print("\n-------------------------")
    print(type(message).__name__)
    print(message.content)