from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

questions = [
    "What is capital of China?",
    "What is capital of India?",
    "What is capital of UAE?",
]

responses = llm.batch(questions)

for response in responses:
    print(response.content)
    print("-" * 50)