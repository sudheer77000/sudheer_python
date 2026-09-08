from langchain_core.tools import tool


class Calculator:

    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b


# Create object
calc = Calculator()

# Access the tool through object
result = calc.add.invoke({
    "a": 10,
    "b": 20
})

print(result)