from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os, openai

load_dotenv()  # looks for .env when running locally

# --- Configure the OpenAI client to point at Groq --------------------------
openai_client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),                    # same key as before
    base_url="https://api.groq.com/openai/v1",            # Groq’s OpenAI‑style URL
    timeout=30,
)

# --------------------------------------------------------------------------

app = FastAPI(title="Mini Chatbot")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

async def groq_complete(prompt: str) -> str:
    if openai_client.api_key is None:                     # graceful fallback
        return f"You said: {prompt!r}. Here's a friendly echo back!"
    try:
        resp = openai_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=128,
        )
        return resp.choices[0].message.content
    except Exception as exc:
        # Bubble up as proper HTTP error for FastAPI
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    reply = await groq_complete(req.message)
    return ChatResponse(reply=reply)
