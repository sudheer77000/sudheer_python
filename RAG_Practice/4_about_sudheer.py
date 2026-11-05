
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from helper_1 import create_vectorstore, ask_from_docs

BASE_DIR = Path(__file__).resolve().parent

sudheer_doc = BASE_DIR / "about_Sudheer_Gundra.txt"

# Load document once
loader = TextLoader(
    str(sudheer_doc),
    encoding="utf-8"
)

docs = loader.load()

# Create or load vector database once
vectorstore = create_vectorstore(docs)

# Interactive question loop
while True:

    question = input(
        "\nAsk your question about Sudheer Gundra "
        "(type 'exit' to stop): "
    )

    if question.lower().strip() == "exit":
        print("Exiting...")
        break

    answer = ask_from_docs(vectorstore, question)

    print("\nAnswer:", answer)
