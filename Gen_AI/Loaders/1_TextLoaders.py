from langchain_community.document_loaders import TextLoader
from pathlib import Path
from helper import ask_from_docs

BASE_DIR = Path.cwd()
TXT_FILE = BASE_DIR / "1_about_sudheer.txt"
loader = TextLoader(TXT_FILE,encoding='utf-8')
docs = loader.load()
print(len(docs))
print("metadata  :  ",docs[0].metadata)
print("page Content  :  ",docs[0].page_content[:100])

while True:
    question = input("\nAbout sudheer Gundra (type 'exit' to stop): ")

    if question.lower() == "exit":
        print("Exiting...")
        break

    answer = ask_from_docs(docs, question)

    print("Answer:", answer)
#print(docs)
