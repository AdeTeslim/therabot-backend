from urllib import response
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq API info
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"  # or "mistral-saba-24b" if terms accepted

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are TheraBot, a friendly, empathetic mental health companion. Offer emotional support, listen attentively, and never give medical advice."},
            {"role": "user", "content": req.message}
        ]
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return {"reply": reply}
    else:
        print(response.json())
        print("Groq response status:", response.status_code)
        print("Groq response body:", response.text)

        return {"reply": "Sorry, something went wrong with TheraBot."}
