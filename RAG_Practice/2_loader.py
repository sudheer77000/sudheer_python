from langchain_community.document_loaders import TextLoader
from pathlib import Path
from helper import ask_from_docs

BASE_DIR = Path.cwd()
sudheer_doc = BASE_DIR / "about_Sudheer_Gundra.txt"
print(sudheer_doc)
loader = TextLoader(sudheer_doc,encoding= 'utf-8')
docs = loader.load()
#print(len(docs))
#print(docs[0].metadata)
#print(docs[0].page_content)

#question = "What is total worth of Sudheer Gundra?"

#answer = ask_from_docs(docs,question)
#print(answer)

while True:
    question = input("\nAsk your question about Sudheer Gundra (type 'exit' to stop): ")

    if question.lower() == "exit":
        print("Exiting...")
        break

    answer = ask_from_docs(docs, question)
    print("\nAnswer:", answer)

