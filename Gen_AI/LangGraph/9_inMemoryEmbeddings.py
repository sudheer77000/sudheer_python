from langgraph.store.memory import InMemoryStore
from langchain.embeddings import init_embeddings
from dotenv import load_dotenv
load_dotenv()


# 1. Create a store configured with an embedding model
store = InMemoryStore(
    index={
        "embed": init_embeddings("openai:text-embedding-3-small"),  # Requires OPENAI_API_KEY
        "dims": 1536,                                            # Dimensions for the embedding model
        "fields": ["$"]                                          # "$" indexes the entire value object
    }
)

# 2. Save your user information
store.put(
    ("students", "stu1"),
    "marks",
    {
        "Science": 92,
        "Hindi": 44,
        "Maths": 100,
        "Telugu": 90,
        "Social": 98,
        "English": 99
    }
)

store.put(
    ("students", "stu1"),
    "details",
    {
        "fName": "Sudheer",
        "lName": "Gundra",
        "Location": "HYD"
    }
)

# 3. Search using a natural language query
result3 = store.search(
    ("students",),
    query="student's performance in Telugu",
    limit=1  # <--- restricts the output to only the top result
)

for item in result3:
    print(f"Key: {item.key} | Score: {item.score} | Value: {item.value}")