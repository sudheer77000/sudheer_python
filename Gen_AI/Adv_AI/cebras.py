import os
from dotenv import load_dotenv
load_dotenv()

from langchain_cerebras import ChatCerebras

llm = ChatCerebras(
    model="qwen-3.8-27b",
    api_key=os.environ["CEREBRAS_API_KEY"],
)

response = llm.invoke("Hello! Explain LangChain in one sentence.")

print(response.content)
