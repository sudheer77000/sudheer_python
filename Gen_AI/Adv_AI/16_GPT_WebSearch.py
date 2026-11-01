
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    tools=[
        {
            "type": "web_search"
        }
    ],
    input="gold rate today india and Dubai. How much differnce between Dubai and India"
)

print(response.output_text)
