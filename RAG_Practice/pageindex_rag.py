
import os
from pathlib import Path
from pageindex import PageIndexClient
from dotenv import load_dotenv
import os
load_dotenv()

# Check API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Set your OPENAI_API_KEY first.")

print("\n=== PAGEINDEX PDF RAG ===")

# Ask for PDF path
pdf_path = input("Enter PDF path: ").strip().strip('"')

if not Path(pdf_path).is_file():
    raise FileNotFoundError("PDF file not found.")

# Initialize PageIndex with cheaper GPT models
client = PageIndexClient(
    index="gpt-5-mini",
    chat="gpt-5-mini"
)

# Build document tree index
print("\nBuilding PageIndex tree...")

result = client.submit_document(
    pdf_path,
    wait=True
)

doc_id = result["doc_id"]

print("Document indexed successfully!")
print("Document ID:", doc_id)

# Interactive question-answering
print("\nAsk questions about your PDF.")
print("Type 'exit' to quit.")

while True:

    question = input("\nYour question: ").strip()

    if question.lower() in ("exit", "quit"):
        print("Goodbye!")
        break

    if not question:
        continue

    try:
        print("\nSearching document...\n")

        answer = client.chat(
            question,
            doc_id=doc_id,
            citations=True
        )

        print("ANSWER:")
        print(answer)

    except Exception as error:
        print("Error:", error)
