from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()



# --------------------------------------------------
# 1. Create embedding model
# --------------------------------------------------

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


# --------------------------------------------------
# 2. Create InMemoryVectorStore
# --------------------------------------------------

vector_store = InMemoryVectorStore(
    embedding=embeddings
)


# --------------------------------------------------
# 3. Add documents
# --------------------------------------------------

documents = [
    Document(
        page_content="Python is a programming language."
    ),
    Document(
        page_content="LangGraph is used to build stateful AI agents."
    ),
    Document(
        page_content="InMemoryVectorStore stores vectors in memory."
    ),
]

vector_store.add_documents(documents)


# --------------------------------------------------
# 4. Search
# --------------------------------------------------

Question = input("Question : ")

results = vector_store.similarity_search(
    Question,
    k=2
)


# --------------------------------------------------
# 5. Print results
# --------------------------------------------------

print("Search results:")

for doc in results:
    print("--------------------")
    print(doc.page_content)