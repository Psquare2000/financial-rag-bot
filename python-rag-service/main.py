from fastapi import FastAPI, Request
from pydantic import BaseModel
import nltk
from models import QueryRequest, QueryResponse
from rag_pipeline import get_answer, load_and_store_documents
import time
from nltk.tokenize import sent_tokenize
from nltk.data import find

nltk.download('punkt_tab')
nltk.download('punkt')

app = FastAPI()

# @app.post("/generate-answer", response_model=QueryResponse)
# def generate_answer(req: QueryRequest):
#     print("Received question:", req.question)
#     return QueryResponse(answer="This is a dummy response for: " + req.question)


@app.post("/query", response_model=QueryResponse)
async def query_api(req: Request):
    t0 = time.time()
    print("🟡 Entered query_api")

    body = await req.json()
    t1 = time.time()
    print("🟢 Parsed JSON body in", round(t1 - t0, 2), "seconds")

    user_question = body.get("question")
    print("📨 User question:", user_question)

    answer_start = time.time()
    answer = await get_answer(user_question)  # <- ✅ Await the async function
    answer_end = time.time()
    print("🔵 get_answer() took", round(answer_end - answer_start, 2), "seconds")

    total_time = time.time() - t0
    print("✅ Total query_api time:", round(total_time, 2), "seconds")

    return {"answer": answer}


@app.post("/load")
async def load_data():
    await load_and_store_documents()
    return {"status": "✅ Documents embedded"}

