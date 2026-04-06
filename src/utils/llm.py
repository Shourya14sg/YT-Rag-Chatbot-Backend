from openai import OpenAI
from dotenv import load_dotenv
from fastapi import HTTPException
from models.chunk_model import Chunk
import os
load_dotenv()
BASE_URL="https://openrouter.ai/api/v1"

ai_model:str="arcee-ai/trinity-large-preview:free"#openai/gpt-oss-120b:free"
#create client
openRouterClient:OpenAI=OpenAI(
    base_url=BASE_URL,
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def translate_chunk(chunk:Chunk)->Chunk:
    try:
        print("starting translation using llm","--",openRouterClient,chunk["text"])
        
        completion=openRouterClient.chat.completions.create(
            model=ai_model,
            messages=[{
                "role": "user",
                "content": f"Translate the following text to English: {chunk["text"]}"
                }
                ],
            )
        print(completion.choices[0].message.content)
        chunk["text"] = completion.choices[0].message.content
        return chunk
    except Exception as e:
        print("error occured in llm",e,type(e))
        raise HTTPException(status_code=504, detail=str(e))