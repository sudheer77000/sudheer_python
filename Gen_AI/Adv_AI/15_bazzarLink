from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

apikey = os.getenv("BAZAAR_LINK_API_KEY")

llm = ChatOpenAI(
    model="auto:free",
    base_url="https://api.bazaarlink.ai/v1",
    api_key=apikey,
    temperature=0
)

response = llm.invoke("Explain About Emaratech Dubai?")
print(response)
print("===" * 25)
print(response.content)