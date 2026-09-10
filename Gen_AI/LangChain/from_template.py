from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple 3 sentences."
)

topic = input("Enter a topic: ")
print("===" * 30)
print(prompt.invoke({"topic": topic}))

response = llm.invoke(
    prompt.invoke({"topic": topic})
)
print("===" * 30)
print(response)
print("===" * 30)
print(response.content)