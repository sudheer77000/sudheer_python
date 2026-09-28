from openai import OpenAI
import ast
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI()


def generate_code(request):
    prompt = f"""
You are a Python code generator.

Generate Python code to solve the user's request.

The code must put the final answer into a variable called `result`.

You may use safe Python standard-library modules such as:
- datetime
- math
- statistics
- re

Do not use:
- os
- subprocess
- socket
- requests
- urllib
- file access
- eval
- exec

User request:
{request}
"""

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    return response.output_text.strip()


import ast


ALLOWED_MODULES = {
    "datetime",
    "math",
}


def validate_code(code):
    tree = ast.parse(code)

    for node in ast.walk(tree):

        # Allow only specific imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in ALLOWED_MODULES:
                    raise ValueError(
                        f"Import not allowed: {alias.name}"
                    )

        elif isinstance(node, ast.ImportFrom):
            if node.module not in ALLOWED_MODULES:
                raise ValueError(
                    f"Import not allowed: {node.module}"
                )

        # Never allow these
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            raise ValueError("Forbidden Python operation")

        # Block dangerous functions
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in {
                    "eval",
                    "exec",
                    "open",
                    "__import__",
                    "compile",
                }:
                    raise ValueError(
                        f"Forbidden function: {node.func.id}"
                    )

    return True

    for node in ast.walk(tree):
        if type(node).__name__ in forbidden:
            raise ValueError("Forbidden Python operation")

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in {
                    "eval",
                    "exec",
                    "open",
                    "__import__"
                }:
                    raise ValueError("Forbidden function")

    return True


def execute_code(code):
    validate_code(code)

    namespace = {}

    exec(
        compile(code, "<ai_generated>", "exec"),
        {"__builtins__": {}},
        namespace
    )

    return namespace["result"]


while True:

    request = input("\nYou: ")

    if request.lower() in {"exit", "quit"}:
        break

    try:
        code = generate_code(request)



        print("\nGenerated Python:")
        print(code)

        result = execute_code(code)

        print("\nResult:")
        print(result)

    except Exception as e:
        print("Error:", e)