from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate
)
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


# -----------------------------
# 1. Initialize the LLM
# -----------------------------
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


#llm = ChatGroq(model="llama-3.1-8b-instant",temperature= 0,max_tokens=100)


# -----------------------------
# 2. Few-shot examples
# -----------------------------
examples = [
    {
        "review": "The food was amazing and the delivery was fast.",
        "sentiment": "Positive",
        "reason": "The customer was satisfied with the food quality and fast delivery."
    },
    {
        "review": "The food was cold and delivery was very late.",
        "sentiment": "Negative",
        "reason": "The customer was unhappy because the food arrived cold and delivery was delayed."
    },
    {
        "review": "The food was tasty, but delivery was late and the food was cold.",
        "sentiment": "Mixed",
        "reason": "The food taste was good, but the customer had a negative experience due to late delivery and cold food."
    }
]


# -----------------------------
# 3. Format each example
# -----------------------------
example_prompt = PromptTemplate.from_template(
    """
Review: {review}

Sentiment: {sentiment}
Reason: {reason}
"""
)


# -----------------------------
# 4. Create Few-Shot Prompt
# -----------------------------
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,

    prefix="""
You are a sentiment analysis assistant.

Analyze the user review and classify the sentiment as:
- Positive
- Negative
- Mixed

Provide a short descriptive reason.
""",

    suffix="""
Review: {review}

Sentiment:
Reason:
""",

    input_variables=["review"]
)


# -----------------------------
# 5. Get input from user
# -----------------------------
review = input("Enter your review: ")


# -----------------------------
# 6. Generate the prompt
# -----------------------------
final_prompt = prompt.invoke({
    "review": review
})


# -----------------------------
# 7. Invoke the LLM
# -----------------------------
response = llm.invoke(final_prompt)


# -----------------------------
# 8. Display the result
# -----------------------------
print("\nLLM Response:")
print(response.content)