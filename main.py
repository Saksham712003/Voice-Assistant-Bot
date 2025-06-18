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
 
