from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import load_chatbot
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://polite-hill-0d3ee1a00.4.azurestaticapps.net"],  # Update to specific domains in production
    # allow_origins=["*"],  # Update to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the chatbot
chatbot = load_chatbot()

# Define request and response models
class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

# def format_response(raw_response: str) -> str:
#     """Format chatbot responses for better readability."""
#     # Split by sentences
#     sentences = raw_response.split(". ")
    
#     # Add bullet points for multiple sentences or paragraphs
#     if len(sentences) > 2:  # If more than two sentences, use bullet points
#         formatted = "\n".join([f"- {sentence.strip()}." for sentence in sentences if sentence.strip()])
#     else:  # For single or short responses, add line breaks
#         formatted = "\n".join([sentence.strip() for sentence in sentences if sentence.strip()])
    
#     # Replace any remaining double newlines
#     formatted = formatted.replace("\n\n", "\n")
    
#     return formatted

@app.get("/")
def read_root():
    return {"message": "Welcome to the Diet Coach Chatbot API!"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Chat endpoint to process user queries."""
    try:
        # Get chatbot response
        answer = chatbot.run(request.question)
        # Format the response
        # formatted_response = format_response(answer)
        return ChatResponse(answer=answer)
    except Exception as e:
        # Handle chatbot or server errors
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500
        )
