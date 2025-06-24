from fastapi import FastAPI
from pydantic import BaseModel
from models import QueryRequest, QueryResponse

app = FastAPI()

@app.post("/generate-answer", response_model=QueryResponse)
def generate_answer(req: QueryRequest):
    print("Received question:", req.question)
    return QueryResponse(answer="This is a dummy response for: " + req.question)
