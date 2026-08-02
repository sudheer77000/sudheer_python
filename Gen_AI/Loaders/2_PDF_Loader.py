from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from helper import ask_from_docs
BASE_DIR = Path.cwd()
PDF_FILE = BASE_DIR / "2_Sudheer_Gundra_Liquor_Shop_Sales_2025.pdf"
loader = PyPDFLoader(PDF_FILE)
docs = loader.load()
print(len(docs))

while True:
    question = input("\nAbout sudheer Gundra Liquor (type 'exit' to stop): ")

    if question.lower() == "exit":
        print("Exiting...")
        break

    answer = ask_from_docs(docs, question)

    print("Answer:", answer)