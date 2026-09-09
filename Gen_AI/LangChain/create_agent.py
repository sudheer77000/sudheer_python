from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.tools import tool


# --------------------------------
# 1. Create a tool
# --------------------------------

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print("========= Addition Method Invoked ===========")
    return a + b


# --------------------------------
# 2. Create the LLM
# --------------------------------

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# --------------------------------
# 3. Create the Agent
# --------------------------------

agent = create_agent(
    model=llm,
    tools=[add]
)


# --------------------------------
# 4. Ask the Agent
# --------------------------------
user_question = input("Please ask Addition Question : ")
result = agent.invoke({
    "messages": [
        ("user", user_question)
    ]
})


# --------------------------------
# 5. Print the final response
# --------------------------------

print(result["messages"][-1].content)