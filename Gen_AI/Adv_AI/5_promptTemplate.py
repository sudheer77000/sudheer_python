from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

prompt = PromptTemplate(
    template="Translate the following sentence to French: {text}",
    input_variables=["text"]
)

result = prompt.invoke({
    "text": "The cat is sitting on the mat."
})

print(result)
print(type(result))

chain = prompt | llm

response = chain.invoke({
    "text": "The cat is sitting on the mat."
})
print(response)
print("++==++" * 20)
print(response.content)