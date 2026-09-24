from langgraph.store.memory import InMemoryStore

# Create a store
store = InMemoryStore()

# Save user information
store.put(
    ("students", "stu1"),
    "marks",
    {
        "Science": 92,
        "Hindi": 44,
        "Maths": 100,
        "Telugu" :90,
        "Social" :98,
        "English" : 99
    }
)

store.put(
    ("students", "stu1"),
    "details",
    {
        "fName" : "Sudheer",
        "lName" : "Gundra",
        "Location" : "HYD"
    }
)

# Get the information
result1 = store.get(
    ("students", "stu1"),
    "marks"
)

result2 = store.get(
    ("students", "stu1"),
    "details"
)

result3 = store.search(
    ("students",),
    query="student's performance in Telugu"
)

print(result1.value)
print(result2.value)
print("##" * 75)
#print(result3.value)
print("##" * 75)
print(result3)