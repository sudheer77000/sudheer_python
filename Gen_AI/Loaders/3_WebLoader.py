from langchain_community.document_loaders import WebBaseLoader
from pathlib import Path
from helper import ask_from_docs

loader = WebBaseLoader("https://www.binghatti.com/en/projects/binghatti-corner")
docs = loader.load()

while True:
    question = input("\nAbout Binghatti Corner (type 'exit' to stop): ")

    if question.lower() == "exit":
        print("Exiting...")
        break

    answer = ask_from_docs(docs, question)

    print("Answer:", answer)