from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

prompt = PromptTemplate.from_template(
    "Explain {topic} in {bullet_points} Bullet Points"
)

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
bullet_points = input("Enter a Bullet points Count: ")

# 4. Invoke the chain
response = chain.invoke({
    "topic": topic,
    "bullet_points": bullet_points
})

# 5. Print response
print(response.content)