from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Message history
messages = []

# First question
first_question = input("First Question Please : ")
messages.append(
    HumanMessage(content=first_question)
)

response = llm.invoke(messages)

messages.append(response)

print("AI:", response.content)


# Second question
second_question = input("Second Question Please : ")
messages.append(
    HumanMessage(content=second_question)
)

response = llm.invoke(messages)

messages.append(response)

print("AI:", response.content)


# See complete history
print("\n--- Message History ---")

for message in messages:
    print(type(message).__name__, ":", message.content)