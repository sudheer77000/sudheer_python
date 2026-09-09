from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

messages = [
    SystemMessage(content="You are a helpful Python teacher."),
    HumanMessage(content="What is a function?")
]

response : AIMessage   = llm.invoke(messages)
print("===" * 10)
print(response)
print("===" * 10)
print(response.content)
print("===" * 10)