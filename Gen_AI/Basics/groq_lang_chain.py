from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
model = ChatGroq(model="llama-3.1-8b-instant",temperature= 0,max_tokens=100)
response = model.invoke("Top 10 elite watch brands in world, only names")
print(response.content)
