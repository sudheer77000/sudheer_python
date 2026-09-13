from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_sarvam import ChatSarvam
from dotenv import load_dotenv
from cursor_client import CursorLLM
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)
import os

load_dotenv()


# Create LLM
llm = ChatOllama(model="qwen2.5:3b",temperature=0)
#llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)
#llm = ChatOpenAI(model="gpt-5.6-luna",temperature=0)
#llm = ChatGroq(model="openai/gpt-oss-20b",temperature=0)
#llm = ChatOpenAI(model="deepseek-v4-flash",temperature=0,api_key=os.getenv("DEEP_API_KEY"),base_url="https://api.deepseek.com")
# Dedicated to Cursor =========== Start =========
#llm = CursorLLM(model="gemini-2.5-flash")
#messages = [
#    SystemMessage(
#        content="""Expert Assistance"""
#    ),
#    HumanMessage(
#       content="""What is UAE? Explain in one sentence.Review"""
#    )
#]
#response = llm.invoke(messages)
#print(response)
# Dedicated to Cursor =========== End =========
# Dedicated to Hugging Face =========== Start =========
#llm = HuggingFaceEndpoint(
#    repo_id="Qwen/Qwen2.5-7B-Instruct-1M",
#    task="text-generation",
#    huggingfacehub_api_token=os.getenv("HF_API_KEY"),
#    temperature=0,
#    max_new_tokens=200,
#)
#chat = ChatHuggingFace(llm=llm)
#response = chat.invoke("What is UAE? Explain in one sentence")
# Dedicated to Hugging Face =========== End =========

# Send a question

response = llm.invoke("What is UAE? Explain in one sentence.")


# Print response
print(response)
print("##" * 75)
print(response.content)