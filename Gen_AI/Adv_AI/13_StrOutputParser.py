from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


# LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# Prompt
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in one sentence."
)


# Output Parser
parser = StrOutputParser()


# LCEL
chain = prompt | llm
#chain = prompt | llm | parser

# Invoke
result = chain.invoke({
    "topic": "RAG"
})


print(result)
print(type(result))
print("##" * 40)
print(parser.invoke(result))
print(type(parser.invoke(result)))