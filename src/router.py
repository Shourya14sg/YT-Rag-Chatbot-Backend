from fastapi import APIRouter, HTTPException
from service import get_transcript, translate_transcript
from utils.rag import upload_to_vector
from models.chunk_model import Chunk
from  youtube_transcript_api import FetchedTranscript
router_yt= APIRouter()

@router_yt.post("{id}")
async def transcript(id: str):
    try:
        transcription:FetchedTranscript = get_transcript(id)
        chunks:Chunk=await translate_transcript(transcription)
        res=await upload_to_vector(chunks)
        return res
    except HTTPException as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Error while fetching transcription:"+str(e))
@router_yt.get("/")
async def askQuestion(question: str):
    return {"question": question}