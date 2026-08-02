from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from pathlib import Path

BASE_DIR = Path.cwd()
TXT_FILE = BASE_DIR / "4_cricket.txt"
loader = TextLoader(TXT_FILE,encoding='utf-8')
docs = loader.load()

embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
splitter = SemanticChunker(embeddings)
chunks = splitter.split_documents(docs)
#print(chunks)


for i,chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print(chunk)