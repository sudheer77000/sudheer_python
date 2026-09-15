from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import httpx

load_dotenv()

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=2,
    top_p = 1,
    top_k = 200,
    stop=[","]
)

#llm = ChatGroq(model="openai/gpt-oss-20b",temperature=0)
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
#                              temperature=0,
#                              top_k = 1,
#                              top_p = 1,
#                              timeout=60
#                              )
# llm = ChatGroq(
#     model="openai/gpt-oss-20b",
#     temperature=0,
#     timeout=60,
#     model_kwargs={
#         "top_k": 1,
#         "top_p": 1
#     }
# )
Question = input("Please Ask The Question : ")
try:
    response = llm.invoke(
        Question
    )
    # print(response)
    # print("SUCCESS")
    # print("==" * 100)
    print(response.content)

except Exception as e:
    print("TIMEOUT / ERROR")
    print("Exception type:", type(e).__name__)
    print("Exception:", e)