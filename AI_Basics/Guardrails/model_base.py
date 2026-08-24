from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def model_based_guardrail(text: str) -> str:
    """Uses an LLM to evaluate content safety. Returns SAFE or UNSAFE."""

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=api_key

    )

    prompt = f"""
You are a content safety guardrail.

Your job is to classify the user's input as SAFE or UNSAFE.

BLOCK the input if it contains or requests content related to:
- Illegal drugs such as heroin, cocaine, methamphetamine, fentanyl
- Instructions for making, buying, selling, or distributing illegal drugs
- Violence, weapons, explosives, or instructions to cause harm
- Self-harm or suicide
- Malware, ransomware, credential theft, password cracking, or DDoS
- Fraud, identity theft, money laundering, or forgery

IMPORTANT:
- If the input only mentions one of these topics, still classify it as UNSAFE.
- Do not try to determine whether the user's intent is educational.
- Return ONLY one word: SAFE or UNSAFE.

User input:
{text}
"""

    result = model.invoke([
        {
            "role": "user",
            "content": prompt
        }
    ])

    return result.content.strip()


print("=== Model-Based Guardrail ===")

# Read user input
user_input = input("\nEnter your question: ")

# Check the input
verdict = model_based_guardrail(user_input)

print(verdict)

# Display result
if verdict == "UNSAFE":
    print("\n❌ BLOCKED")
    print("Detected as UNSAFE")

else:
    print("\n✅ ALLOWED")
    print("Detected as SAFE")