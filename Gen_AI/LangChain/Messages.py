from langchain_ollama import ChatOllama
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage
)
from langchain_core.tools import tool


# ============================================================
# 1. Define a Tool
# ============================================================

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


# ============================================================
# 2. Create LLM
# ============================================================

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

llm_with_tools = llm.bind_tools([add])


# ============================================================
# 3. Message History
# ============================================================

messages = []


# ============================================================
# 4. HUMAN MESSAGE
# ============================================================

humanMsg = input("Human Question : ")

human_msg = HumanMessage(
    content=humanMsg
)

messages.append(human_msg)

print("\n1️⃣ HUMAN MESSAGE")
print(messages[-1])


# ============================================================
# 5. AI MESSAGE
# ============================================================

ai_msg = llm_with_tools.invoke(messages)

messages.append(ai_msg)

print("\n2️⃣ AI MESSAGE")
print(ai_msg)

print("\nTool calls:")
print(ai_msg.tool_calls)


# ============================================================
# 6. TOOL MESSAGE
# ============================================================

if ai_msg.tool_calls:

    tool_call = ai_msg.tool_calls[0]

    result = add.invoke(tool_call["args"])

    tool_msg = ToolMessage(
        content=str(result),
        tool_call_id=tool_call["id"]
    )

    messages.append(tool_msg)

    print("\n3️⃣ TOOL MESSAGE")
    print(tool_msg)


# ============================================================
# 7. Send complete history back to LLM
# ============================================================

final_ai_msg = llm_with_tools.invoke(messages)

messages.append(final_ai_msg)

print("\n4️⃣ FINAL AI MESSAGE")
print(final_ai_msg)


# ============================================================
# 8. COMPLETE MESSAGE HISTORY
# ============================================================

print("\n\n========== MESSAGE HISTORY ==========")

for i, message in enumerate(messages):

    print(f"\nMessage {i + 1}")
    print("Type:", type(message).__name__)
    print("Content:", message.content)

    if hasattr(message, "tool_calls"):
        if message.tool_calls:
            print("Tool Calls:", message.tool_calls)