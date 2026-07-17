from fastapi import APIRouter
from pydantic import BaseModel
import ollama


router = APIRouter()


# Connect to Ollama through Cloudflare Tunnel
client = ollama.Client(
    host="https://about-dollars-ice-train.trycloudflare.com"
)



class ChatRequest(BaseModel):

    resume_text: str

    message: str





@router.post("/chat")
async def chat(data: ChatRequest):

    try:

        prompt = f"""

You are an AI Resume Assistant.

Answer questions based on this resume.

Resume:

{data.resume_text}


Question:

{data.message}

"""


        response = client.chat(

            model="llama3.2",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )


        return {

            "reply": response["message"]["content"]

        }



    except Exception as e:

        print("OLLAMA CHAT ERROR:", e)

        return {

            "reply": str(e)

        }