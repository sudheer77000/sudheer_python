
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from autobatcher import BatchOpenAI
from openai import OpenAI
load_dotenv()

api_key = os.getenv("DOUBLEWORD_API_KEY")


client = OpenAI(
    api_key=api_key,
    base_url="https://api.doubleword.ai/v1"
)

response = client.chat.completions.create(
    model="Qwen/Qwen3-14B-FP8",
    messages=[
        {"role": "user", "content": "Thank you"}
    ]
)

print(response.choices[0].message.content)