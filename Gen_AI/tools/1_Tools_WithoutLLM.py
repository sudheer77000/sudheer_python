from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

result = add.invoke({"a": 10, "b": 20})

print(result)