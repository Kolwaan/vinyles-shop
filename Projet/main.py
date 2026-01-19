from typing import Union

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session


from models.database import Base, get_db, engine
from schemas.vinyl import VinylCreate
from models.vinyl import Vinyl

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/vinyls/")
def create_vinyl(vinyl: VinylCreate, db: Session = Depends(get_db)):
    vinyl_to_create = Vinyl(
        title = vinyl.title,
        artist = vinyl.artist,
        year = vinyl.year,
        genre = vinyl.genre
    )
    db.add(vinyl_to_create)
    db.commit()
    db.refresh(vinyl_to_create)
    return vinyl_to_create