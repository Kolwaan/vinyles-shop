from pydantic import BaseModel
from typing import Union



class VinylCreate(BaseModel):
    title: str
    artist: str
    year: int | None
    genre: str | None
