from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables (for OpenAI key)
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load existing vector DB
client = PersistentClient(path="vector_store")
collection = client.get_or_create_collection(name="finance_docs")

# Define embedder
def get_embedding(text):
    response = openai_client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

# Sample user query
query = "What is ELSS and how does it provide tax benefits?"

# Generate embedding for query
query_embedding = get_embedding(query)

# Query the vector DB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3  # top 3 most relevant
)

# Show the relevant documents
for i, doc in enumerate(results['documents'][0]):
    print(f"\n🔍 Match #{i+1}:\n{doc}")
