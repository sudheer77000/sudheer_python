from typesafe_sdk import TypeSafeClient, Choice, Score, Noul
import os
from dotenv import load_dotenv
load_dotenv()


# Create Jev client
client = TypeSafeClient()


# Get review from command line
review = input("Enter product review: ")


# Send review to Jev
result = client.system_one(
    state=review,

    questions={

        "sentiment": Choice(
            instructions="What is the overall sentiment of this review?",
            criteria={
                "positive": "Customer is generally happy",
                "neutral": "Customer has mixed or neutral feedback",
                "negative": "Customer is generally unhappy",
            },
        ),

        "rating": Score(
            instructions="How positive is this review?",
            criteria=[
#                "Very negative",
                 "Negative",
#                "Neutral",
                 "Positive",
#                "Very positive",
            ],
        ),

        "detailedReview": Noul(
            instructions="Would customer provided detailed review?"
        ),
    },
)


# Display result
print("\n===== JEV RESULT =====")

print("Review:", review)

print("Sentiment:",
      result.answers["sentiment"].choice)

print("Score:",
      result.answers["rating"].score)

print("Detailed Review:",
      result.answers["detailedReview"].noul)

print("==" * 75)
print(result)
