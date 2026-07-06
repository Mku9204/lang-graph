from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat.chat_file import initial_chat


class ChatRequest(BaseModel):
    message: str


app=FastAPI(title="Chat Api Docs",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message":'Running'}

@app.post('/chat', response_model=None)
def create_chat(request: ChatRequest):
    user_id=1
    response = initial_chat(request.message,user_id)
    return {"message": response}