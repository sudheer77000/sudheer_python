from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional translator."),
    ("human", "Translate the following sentence to French: {text}")
])

result = prompt.invoke({
    "text": "The cat is sitting on the mat."
})

print(result)
print(type(result))