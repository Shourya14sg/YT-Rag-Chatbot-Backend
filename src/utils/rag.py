from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.chunk_model import Chunk
from langchain_openai import OpenAIEmbeddings
from langchain_classic.embeddings import CacheBackedEmbeddings  
from langchain_classic.storage import LocalFileStore
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
import asyncio
import os

text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_text(text)

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="text-embedding-3-small"
    )#)
store = LocalFileStore("./cache/")
#embedding
        # Store persists embeddings to the local filesystem
        # This isn't for production use, but is useful for loca
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
            embeddings,
            store,
            namespace=embeddings.model
)
async def upload_to_vector(chunks:list[Chunk]):
    print(chunks,"----------")
    try:
        #convert to document
        # Step 1: convert to documents
        documents = [
            Document(
                page_content=chunk.text,
                metadata={
                    "start_time": chunk.start_time,
                    # "video_id": chunk.get("video_id")
                }
            )
            for chunk in chunks
        ]

        # Step 2: extract text for embedding
        texts = [doc.page_content for doc in documents]
        # This computes + caches embeddings
        await cached_embedder.aembed_documents(texts)
                # This actually creates a vector index
        vectorstore = await asyncio.to_thread(
            FAISS.from_documents,
            documents,
            cached_embedder,
        )
        await asyncio.to_thread(vectorstore.save_local, "./faiss_index")

        # cached_embedder.aembed_documents(documents)
        return {"status": "success", "chunks": len(chunks)}
    except Exception as e:
        print("error occured in Rag",e,type(e))
        raise HTTPException(status_code=504, detail=str(e))