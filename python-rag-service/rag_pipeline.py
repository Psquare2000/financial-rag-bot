import os
import chromadb
import chromadb
import time
import nltk
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
from uuid import uuid4

from nltk.tokenize import sent_tokenize

load_dotenv()  # Optional: Load from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

client = chromadb.PersistentClient(path="./vector_store")
# openai_client = OpenAI()
openai_client = AsyncOpenAI()

collection = client.get_or_create_collection(name="finance_docs")
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "data/elss_guide.txt")

file_path = os.path.join(os.path.dirname(__file__), "data", "elss_guide.txt")

# Get embeddings via OpenAI
async def embed(texts):
    print(f"📨 rag_pipeline.embed - Requesting embeddings for {len(texts)} text(s)")

    t0 = time.time()
    response = await openai_client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    t1 = time.time()

    print("📦 data received from OpenAI")
    print("✅ rag_pipeline.embed - Completed")
    print(f"⏱️ Embedding API call took {round(t1 - t0, 2)} seconds")

    return [record.embedding for record in response.data]


def smart_chunk(text, max_sentences=5, overlap=2):
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(text)
    chunks = []
    i = 0
    while i < len(sentences):
        chunk = sentences[i:i+max_sentences]
        chunks.append(" ".join(chunk))
        i += max_sentences - overlap
    return chunks


async def load_and_store_documents():
    print("Checking file:", file_path)
    print("Exists?", os.path.exists(file_path))
    print("Is file?", os.path.isfile(file_path))
    print("Resolved path:", file_path)
    print("📥 rag_pipeline.load_and_store_documents")

    # Load text file 
    with open(file_path, "r") as f:
        raw_text = f.read()

    # Chunking with sentence-awareness and overlap
    chunks = smart_chunk(raw_text, max_sentences=5, overlap=2)
    print(f"📦 Total chunks created: {len(chunks)}")

    # Embed and store in vector DB
    embeddings = await embed(chunks)
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[str(uuid4()) for _ in chunks]
    )

    print("✅ Documents embedded and stored in ChromaDB.")


async def get_answer(question):
    print("📌 rag_pipeline.get_answer")

    start_time = time.time()

    # 1. Embed the user query
    t0 = time.time()
    query_embedding = (await embed([question]))[0]
    t1 = time.time()
    print(f"⏱ embed() took {round(t1 - t0, 2)}s")

    # 2. Search ChromaDB (still sync)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    t2 = time.time()
    print(f"⏱ ChromaDB query took {round(t2 - t1, 2)}s")

    # 3. Concatenate documents
    context = "\n".join(results["documents"][0])
    t3 = time.time()
    print(f"⏱ Context concatenation took {round(t3 - t2, 2)}s")

    # 4. Call OpenAI Chat Completion (async)
    response = await openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial assistant."},
            {"role": "user", "content": f"Use the context below to answer:\n\n{context}\n\nQ: {question}"}
        ]
    )
    t4 = time.time()
    print(f"⏱ OpenAI chat call took {round(t4 - t3, 2)}s")

    total = round(t4 - start_time, 2)
    print(f"✅ Total get_answer() time: {total}s")

    return response.choices[0].message.content
