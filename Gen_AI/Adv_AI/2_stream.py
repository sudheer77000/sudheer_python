from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

Question = input("Please Enter your Question : ")

for chunk in llm.stream(Question):
    print(chunk.content, end="", flush=True)

print()