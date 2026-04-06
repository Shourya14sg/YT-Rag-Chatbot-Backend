from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import HTTPException
from youtube_transcript_api import FetchedTranscript, FetchedTranscriptSnippet
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from utils.llm import translate_chunk
from utils.utils import create_time_based_chunks
from models.chunk_model import Chunk
import asyncio
def get_transcript(video_id) -> FetchedTranscript:
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript: FetchedTranscript=ytt_api.fetch(
            video_id,
            languages=("en", "hi")
            )
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def translate_transcript(transcript:FetchedTranscript)->str:
    try:
        snippets:list[FetchedTranscriptSnippet] = transcript.snippets
        language_code = transcript.language_code
        #Step 1 : chunking
        chunks:list[Chunk] = create_time_based_chunks(snippets)
        # print(language_code,"----code------")
        # Step 2: translate if needed
        if not language_code.startswith("en"):
            #translated_text =await translate_chunk(text)  #bad for large text but good for small
            translated_chunks=await asyncio.gather(
                *(translate_chunk(chunk) for chunk in chunks)
            )   #concureent chunk fire
        else:
            translated_chunks = chunks
        return translated_chunks
        """ native approach but we have smarter way for chunking
        # Step 1: convert to text
        text = " ".join([s.text for s in transcript.snippets])    # s["text"] is not dictionary it is list here
        # Step 2: clean

        #chunk
        chunks = chunk_text(text)
        # Step 3: translate if needed
        if not transcript.language_code.startswith("en"):
            #translated_text =await translate_chunk(text)  #bad for large text but good for small
            translated_chunks=await asyncio.gather(
                *(translate_chunk(chunk) for chunk in chunks)
            )   #concureent chunk fire
        else:
            translated_chunks = chunks
        return translated_chunks
        """
    except Exception as e:
        raise e