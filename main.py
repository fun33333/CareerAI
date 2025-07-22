from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_files.main_agent import main_agent
from agents import Runner

app = FastAPI()

# CORS enable for all origins (for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list = []  # Optional: for conversation context

class ChatResponse(BaseModel):
    reply: str

IRRELEVANT_KEYWORDS = [
    "sex", "religion", "politics", "joke", "adult", "personal info", "address", "phone", "credit card"
]

def is_irrelevant(message: str) -> bool:
    return any(word in message.lower() for word in IRRELEVANT_KEYWORDS)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if is_irrelevant(request.message):
        return ChatResponse(reply="Sorry, main sirf career guidance ke liye hoon. Faltu ya personal sawalon ka jawab nahi de sakta.")
    # Prepare history for agent (if needed)
    history = request.history or []
    history.append({"role": "user", "content": request.message})
    try:
        result = await Runner.run(
            starting_agent=main_agent,
            input=history
        )
        response = result.final_output
        return ChatResponse(reply=response)
    except Exception as e:
        return ChatResponse(reply=f"Sorry, error: {e}")