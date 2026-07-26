from langchain_community.document_loaders import WebBaseLoader
from helper import ask_from_docs

loader = WebBaseLoader("https://www.carwale.com/tata-cars/punch")
docs = loader.load()

while True:
    question = input("\nAsk your question about Tata Punch (type 'exit' to stop): ")

    if question.lower() == "exit":
        print("Exiting...")
        break

    answer = ask_from_docs(docs, question)

    print("Answer:", answer)