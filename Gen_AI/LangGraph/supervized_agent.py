from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


# ------------------------------------------------
# LLM
# ------------------------------------------------

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# ------------------------------------------------
# Specialist Agent 1
# ------------------------------------------------

def math_agent(question):

    prompt = f"""
    You are a Math Specialist.

    Solve this question:

    {question}
    """

    response = llm.invoke(prompt)

    return response.content


# ------------------------------------------------
# Specialist Agent 2
# ------------------------------------------------

def general_agent(question):

    prompt = f"""
    You are a General Knowledge Specialist.

    Answer this question:

    {question}
    """

    response = llm.invoke(prompt)

    return response.content


# ------------------------------------------------
# Supervisor
# ------------------------------------------------

def supervisor(question):

    prompt = f"""
    You are a Supervisor.

    Decide which specialist should answer the question.

    Available specialists:

    MATH
    GENERAL

    Return ONLY one word.

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    decision = response.content.strip().upper()

    return decision


# ------------------------------------------------
# Main Multi-Agent System
# ------------------------------------------------

question = input("User: ")

# Supervisor decides
decision = supervisor(question)

print("\nSupervisor selected:", decision)


# Handoff to specialist
if "MATH" in decision:

    result = math_agent(question)

elif "GENERAL" in decision:

    result = general_agent(question)

else:

    result = "Supervisor could not decide."


print("\nFinal Answer:")
print(result)