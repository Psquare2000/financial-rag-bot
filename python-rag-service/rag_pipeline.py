import os
import chromadb
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()  # Optional: Load from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

client = chromadb.PersistentClient(path="./vector_store")
openai_client = OpenAI()

collection = client.get_or_create_collection(name="finance_docs")
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data/elss_guide.txt")

file_path = os.path.join(os.path.dirname(__file__), "data", "elss_guide.txt")
print("Checking file:", file_path)

print("Exists?", os.path.exists(file_path))
print("Is file?", os.path.isfile(file_path))

print("Resolved path:", file_path)


# Load text file
with open(file_path, "r") as f:
    raw_text = f.read()

# Split into chunks (naive split for now)
chunks = [raw_text[i:i+300] for i in range(0, len(raw_text), 300)]

# Get embeddings via OpenAI
def embed(texts):
    response = openai_client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )

    # Print just the first embedding for sanity check
    print("data obj", response.data)
    # print("First Embedding Vector:", response.data[0].embedding)

    return [record.embedding for record in response.data]


# Add to vector store
embeddings = embed(chunks)
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[str(uuid4()) for _ in chunks]
)

print("✅ Documents embedded and stored in ChromaDB.")


def get_answer(question):
    # Embed the user query
    query_embedding = embed([question])[0]

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # Concatenate documents
    context = "\n".join(results["documents"][0])

    # Call OpenAI with context + question
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial assistant."},
            {"role": "user", "content": f"Use the context below to answer:\n\n{context}\n\nQ: {question}"}
        ]
    )

    return response.choices[0].message.content

