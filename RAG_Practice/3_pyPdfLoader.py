from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from helper import ask_from_docs

BASE_DIR = Path.cwd()
sudheer_Sales_Doc = BASE_DIR / "Sudheer_Automobiles_Sales_Report.pdf"
print(sudheer_Sales_Doc)
loader = PyPDFLoader(sudheer_Sales_Doc)
docs = loader.load()

while True:
    question = input("\nAsk your question about Sudheer Gundra Automobiles (type 'exit' to stop): ")

    if question.lower() == "exit":
        print("Exiting...")
        break

    answer = ask_from_docs(docs, question)

    print("Answer:", answer)