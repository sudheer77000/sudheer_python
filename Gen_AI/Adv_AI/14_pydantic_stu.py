from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


class AnimalInfo(BaseModel):
    subject: str = Field(description="Name of the animal")
    action: str = Field(description="What the animal is doing")
    location: str = Field(description="Where the animal is")


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

structured_llm = llm.with_structured_output(AnimalInfo)

result = structured_llm.invoke(
    "The cat is sitting on the mat."
)

print(result)
print(result.subject)
print(result.action)
print(result.location)

# Convert Structured Output → JSON
json_output = result.model_dump_json(indent=4)

print("\nJSON Output:")
print(json_output)