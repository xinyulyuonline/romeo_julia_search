from pydantic import BaseModel

class postData(BaseModel):
    filename: str = "romeo_julia_chunks"
    chunks: int = 90

class askData(BaseModel):
    question: str
    chunks: int = 1