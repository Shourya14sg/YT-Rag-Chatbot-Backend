from pydantic import BaseModel

class Chunk(BaseModel):
    text: str
    start_time: float
    # duration: float