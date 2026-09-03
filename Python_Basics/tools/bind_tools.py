from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

@tool
def withdraw_amount(amount: int,accountNo: str) -> str:
    """This Tool is useful for to withdram an amount from Bank Account"""
    print(f"Amount : {amount} is debited from Account {accountNo}")
    return "Amount : " + str(amount) + " is debited from Account : " + accountNo

@tool
def deposit_amount(amount: int,accountNo: str) -> str:
    """This Tool is useful for to deposit an amount to Bank Account"""
    print(f"Amount : {amount} is created to Account {accountNo}")
    return "Amount : " + str(amount) + " is credited to Account : " + accountNo

model = ChatOllama(
    model="qwen2.5:3b",
    temperature=1
)

model_with_tools = model.bind_tools(
    [withdraw_amount, deposit_amount]
)

user_request = input("Please Enter User Request : ")

response = model_with_tools.invoke(
    user_request
)

print(response)

tool_call = response.tool_calls[0]
method_name = tool_call["name"]
arguments = tool_call["args"]

print("Tool name:", method_name)
print("Arguments:", arguments)

# 1. Assuming you have your tools and tool_map ready
tools = [withdraw_amount, deposit_amount]
tool_map = {tool.name: tool for tool in tools}

tool_result = tool_map[method_name].invoke(arguments)
print(tool_result)

final_response = model.invoke([
    {
        "role": "user",
        "content": user_request
    },
    response,
    {
         "role": "tool",
         "content": str(tool_result),
        "tool_call_id": tool_call["id"]
    }
    ])

print("*"*100)
print(final_response.content)
print("*"*100)
