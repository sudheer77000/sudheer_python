from cursor_client import CursorLLM

from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)


llm = CursorLLM(
    model="gemini-2.5-flash"
)

User_Review = input("Please Enter your Review : ")

messages = [
    SystemMessage(
        content="""You are an expert customer service representative. Analyze the user's comment, determine its sentiment, explain the reasoning behind your classification, and draft a professional response.

Task Instructions

Analyze Sentiment: Classify the comment strictly as POSITIVE, NEGATIVE, or NEUTRAL.

Identify Reason: Provide a 1-2 sentence explanation detailing why the comment falls into that category (e.g., product defect, fast delivery, general inquiry).

Output Format

Review: [ POSITIVE | NEGATIVE | NEUTRAL ]

Reason: [ Identify Reason ]
"""
    ),
    HumanMessage(
        content=User_Review
    )
]


response = llm.invoke(messages)
print("===" * 30)
print(response)
print("===" * 30)