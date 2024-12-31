from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import load_chatbot
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize the chatbot
chatbot = load_chatbot()

# Define request and response models
class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
@app.get("/")
def read_root():
    return {"message": "Welcome to the Diet Coach Chatbot API!"}
# Define API endpoint for chat
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Run the chatbot and return the response
    answer = chatbot.run(request.question)
    return ChatResponse(answer=answer)
