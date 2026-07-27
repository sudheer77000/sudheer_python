from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond in less than 10 words"),
    ("human", "Explain {topic}.")
])

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=1,
    top_k=10,
    top_p=0.9,
    num_predict=500,
    repeat_penalty=1.1,
    num_ctx=500,
    #seed=4
)

# 3. Create chain
chain = prompt | llm

topic = input("Enter a topic: ")

# 4. Invoke the chain
response = chain.invoke({
    "topic": topic
})

# 5. Print response
print(response.content)