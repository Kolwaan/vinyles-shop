from pydantic import BaseModel
from typing import Optional



class VinylCreate(BaseModel):
    title: str
    artist: str
    year: Optional[int]
    genre: Optional[str]
