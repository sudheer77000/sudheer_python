from langchain_ollama import ChatOllama
from langchain_core.tools import tool


# ============================================================
# 1. Create a Tool
# ============================================================

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print(f"\n🔧 TOOL EXECUTION: add({a}, {b})")
    return a + b


@tool
def sub(a: int, b: int) -> int:
    """Substraction two numbers."""
    print(f"\n🔧 TOOL EXECUTION: add({a}, {b})")
    return a - b

# ============================================================
# 2. Create Qwen 2.5 3B
# ============================================================

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# ============================================================
# 3. Bind the tool to Qwen
# ============================================================

llm_with_tools = llm.bind_tools([add,sub])

print("====" * 30)
print(llm_with_tools)
print("====" * 30)


# ============================================================
# 4. User question
# ============================================================

user_question = input("User Question : ")

print("👤 USER:")
print(user_question)


# ============================================================
# 5. Ask Qwen
# ============================================================

ai_msg = llm_with_tools.invoke(user_question)

print("\n🤖 QWEN RESPONSE:")
print(ai_msg)


# ============================================================
# 6. Check whether Qwen requested a tool
# ============================================================

if ai_msg.tool_calls:

    print("\n📞 TOOL CALL:")
    print(ai_msg.tool_calls)

    tool_call = ai_msg.tool_calls[0]

    # ========================================================
    # 7. Execute the tool
    # ========================================================

    tool_result = add.invoke(tool_call["args"])

    print("\n🔧 TOOL RESULT:")
    print(tool_result)

    # ========================================================
    # 8. Send result back to Qwen
    # ========================================================

    final_msg = llm_with_tools.invoke([
        user_question,
        ai_msg,
        {
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": str(tool_result)
        }
    ])

    # ========================================================
    # 9. Final answer
    # ========================================================

    print("\n🤖 FINAL ANSWER:")
    print(final_msg.content)

else:

    print("\n🤖 QWEN ANSWERED DIRECTLY:")
    print(ai_msg.content)