from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your domain in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # your key
)

class Prompt(BaseModel):
    text: str

@app.post("/chat")
async def chat(prompt: Prompt):
    response = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "VoiceWebBot"
        },
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt.text}],
        max_tokens=2048
    )
    return {"response": response.choices[0].message.content}
 
