from fastapi import FastAPI, Request
from pydantic import BaseModel
from models import QueryRequest, QueryResponse
from rag_pipeline import get_answer

app = FastAPI()

@app.post("/generate-answer", response_model=QueryResponse)
def generate_answer(req: QueryRequest):
    print("Received question:", req.question)
    return QueryResponse(answer="This is a dummy response for: " + req.question)

@app.post("/query")
async def query_api(req: Request):
    body = await req.json()
    user_question = body.get("question")
    answer = get_answer(user_question)
    return {"answer": answer}
