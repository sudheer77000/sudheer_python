from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama


@tool
def add(num1: float,num2: float) -> float:
     """Addition Of Two Numbers"""
     print("Add Method Initiated.....")
     return num1 + num2

@tool
def sub(num1: float,num2: float) -> float:
    """Substraction Of Two Numbers"""
    print("Sub Method Initiated.....")
    return num1 - num2

@tool
def mul(num1: float,num2: float) -> float:
    """Multiplication Of Two Numbers"""
    print("Mul Method Initiated.....")
    return num1 * num2

@tool
def div(num1: float,num2: float) -> float:
    """Division Of Two Numbers"""
    print("Div Method Initiated.....")
    return num1 / num2

from langchain.tools import tool

@tool
def handle_unknown_topic(query: str) -> str:
    """
    MANDATORY TOOL FOR IRRELEVANT QUESTIONS.
    If the user asks about ANY topic other than math or calculations, you MUST call this tool. 
    Pass the user's exact query as the argument.
    """
    return "Out Of Scope Question"

#ai_obj = AICalculator()

model = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

agent = create_agent(
    model=model,
    tools=[
        add,
        sub,
        mul,
        div,
        handle_unknown_topic
    ]
)
Query = input("Please Enter The Calculator Query : ")
print("🧠 Agent is thinking....")

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": Query
        }
    ]
})

#print(response)
print("=*=*" * 30)
print(response["messages"][-1].content)