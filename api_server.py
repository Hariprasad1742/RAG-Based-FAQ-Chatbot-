from fastapi import FastAPI
from pydantic import BaseModel

# Import RAG functions
from rag_chatbot import generate_rag_response

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_faq(query: Query):
    response = generate_rag_response(query.question)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
