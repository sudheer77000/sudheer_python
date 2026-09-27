
from langgraph.store.memory import InMemoryStore
from langmem import create_memory_store_manager
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


# --------------------------------------------------
# 1. Create the model
# --------------------------------------------------

model = ChatOpenAI(
    model="gpt-4o-mini"
)


# --------------------------------------------------
# 2. Create the in-memory store
# --------------------------------------------------

store = InMemoryStore()


# --------------------------------------------------
# 3. Create memory manager
# --------------------------------------------------

memory_manager = create_memory_store_manager(
    model,
    namespace=("users", "user123"),
    store=store,
)


# --------------------------------------------------
# 4. Give the manager a conversation
# --------------------------------------------------

memory_manager.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Hi! My name is John and I love Python."
            }
        ]
    }
)


# --------------------------------------------------
# 5. Look at what was saved
# --------------------------------------------------

print("\nSaved memories:")

memories = store.search(
    ("users", "user123")
)

for memory in memories:
    print("Key:", memory.key)
    print("Value:", memory.value)
    print("-" * 40)

