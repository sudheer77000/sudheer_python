from langchain_core.tools import tool
from langchain_ollama import ChatOllama


# ============================================================
# TOOL 1 - ADD
# ============================================================

@tool
def add(num1: int, num2: int) -> int:
    """Add two numbers."""
    
    print(f"\n[TOOL EXECUTING] add({num1}, {num2})")
    
    result = num1 + num2
    
    print(f"[TOOL RESULT] {result}")
    
    return result


# ============================================================
# TOOL 2 - SUBTRACT
# ============================================================

@tool
def subtract(num1: int, num2: int) -> int:
    """Subtract num2 from num1."""
    
    print(f"\n[TOOL EXECUTING] subtract({num1}, {num2})")
    
    result = num1 - num2
    
    print(f"[TOOL RESULT] {result}")
    
    return result


# ============================================================
# CREATE MODEL
# ============================================================

model = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# ============================================================
# BIND TOOLS TO MODEL
# ============================================================

model_with_tools = model.bind_tools(
    [add, subtract]
)


# ============================================================
# USER QUESTION
# ============================================================

user_question = "What is 20 + 10?"


# ============================================================
# STEP 1 - SEND QUESTION TO LLM
# ============================================================

print("\n==============================")
print("STEP 1 - USER QUESTION")
print("==============================")

print(user_question)


response = model_with_tools.invoke(
    user_question
)


# ============================================================
# STEP 2 - CHECK LLM RESPONSE
# ============================================================

print("\n==============================")
print("STEP 2 - LLM RESPONSE")
print("==============================")

print(response)


# ============================================================
# STEP 3 - CHECK FOR TOOL CALL
# ============================================================

if response.tool_calls:

    print("\n==============================")
    print("STEP 3 - TOOL CALL DETECTED")
    print("==============================")

    tool_call = response.tool_calls[0]

    print("Tool name:", tool_call["name"])
    print("Arguments:", tool_call["args"])


    # ========================================================
    # STEP 4 - EXECUTE TOOL
    # ========================================================

    print("\n==============================")
    print("STEP 4 - EXECUTING TOOL")
    print("==============================")


    if tool_call["name"] == "add":

        tool_result = add.invoke(
            tool_call["args"]
        )

    elif tool_call["name"] == "subtract":

        tool_result = subtract.invoke(
            tool_call["args"]
        )

    else:

        raise ValueError(
            f"Unknown tool: {tool_call['name']}"
        )


    # ========================================================
    # STEP 5 - SEND TOOL RESULT BACK TO LLM
    # ========================================================

    print("\n==============================")
    print("STEP 5 - TOOL RESULT")
    print("==============================")

    print(tool_result)


    # ========================================================
    # STEP 6 - ASK LLM FOR FINAL ANSWER
    # ========================================================

    print("\n==============================")
    print("STEP 6 - FINAL LLM RESPONSE")
    print("==============================")


    final_response = model.invoke([
        {
            "role": "user",
            "content": user_question
        },
        response,
        {
            "role": "tool",
            "content": str(tool_result),
            "tool_call_id": tool_call["id"]
        }
    ])


    print(final_response.content)


else:

    print("\nLLM did not request a tool.")

    print("\nFinal Answer:")
    print(response.content)