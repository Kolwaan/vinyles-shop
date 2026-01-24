from pydantic import BaseModel
from typing import Union
from datetime import datetime



class VinylCreate(BaseModel):
    title: str
    artist: str
    year: int | None
    genre: str | None

class VinylOut(BaseModel):
    id: int
    title: str
    artist: str
    year: int | None
    genre: str | None
    added_at: datetime

    class Config:
        orm_mode = True


