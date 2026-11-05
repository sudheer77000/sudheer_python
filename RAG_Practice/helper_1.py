
from dotenv import load_dotenv
from pathlib import Path

from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vectorstore(docs):

    # Check whether persistent database exists
    if (DB_DIR / "chroma.sqlite3").exists():

        print("Loading existing Chroma database...")

        vectorstore = Chroma(
            persist_directory=str(DB_DIR),
            embedding_function=embeddings
        )

    else:

        print("Creating new Chroma database...")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(DB_DIR)
        )

        print("Chroma database created successfully!")

    return vectorstore


def ask_from_docs(vectorstore, question):

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    relevant_docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in relevant_docs
    )

    prompt = ChatPromptTemplate.from_template("""
Answer the question using only the given context.

Context:
{context}

Question:
{question}

If the answer is not available in the context, say:
"I don't know based on the provided document."
""")

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "context": context,
        "question": question
    })



BASE_DIR = Path(__file__).resolve().parent
CACHE_DB = BASE_DIR / "llm_cache.db"

# Enable persistent LLM cache
set_llm_cache(
    SQLiteCache(
        database_path=str(CACHE_DB),
        allowed_objects="messages"
    )
)