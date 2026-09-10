from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful banking assistant."),
    ("human", "top 10 cities in UAE?")
])

response = llm.invoke(prompt.invoke({}))

print(response.content)