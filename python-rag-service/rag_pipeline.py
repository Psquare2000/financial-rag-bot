import os
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()  # Optional: Load from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./vector_store"))

collection = client.get_or_create_collection(name="finance_docs")

# Load text file
with open("data/elss_guide.txt", "r") as f:
    raw_text = f.read()

# Split into chunks (naive split for now)
chunks = [raw_text[i:i+300] for i in range(0, len(raw_text), 300)]

# Get embeddings via OpenAI
def embed(texts):
    import openai
    openai.api_key = openai_api_key
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts
    )
    return [d["embedding"] for d in response["data"]]

# Add to vector store
embeddings = embed(chunks)
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[str(uuid4()) for _ in chunks]
)

print("✅ Documents embedded and stored in ChromaDB.")
