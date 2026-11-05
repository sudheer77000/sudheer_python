from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    tools=[
        {
            "type": "code_interpreter",
            "container": {
                "type": "auto"
            }
        }
    ],
    input="""
    Calculate the total and average of:
    100, 200, 300, 400, 500.

    Use Python to perform the calculation.
    """
)

print(response.output_text)