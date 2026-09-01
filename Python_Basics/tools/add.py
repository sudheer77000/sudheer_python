from langchain_core.tools import tool

def multiply(a: int, b: int) -> int:
    return a * b

@tool
def multiply_tool(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

a = int(input("Please Enter Num1 : "))
b = int(input("Please Enter Num1 : "))
result = multiply(a, b) 
print("Product Of two Numbers : ", result)

result1 = multiply_tool.invoke({"a": a, "b": b}) 
print("Product Of two Numbers Tools Result : ", result1)
