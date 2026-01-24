from typing import Union

from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session


from models.database import Base, get_db, engine
from schemas.vinyl import VinylCreate, VinylOut

from controllers.vinyl import create_vinyl, list_vinyls, get_vinyl
app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/vinyls")
def list_vinyls_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_vinyls(skip, limit, db)

@app.get("/vinyls/{vinyl_id}", response_model = VinylOut)
def get_vinyl_route(vinyl_id:int, db: Session = Depends(get_db)):
    try: 
        vinyl =  get_vinyl(vinyl_id, db)
    except Exception as e:
        return str(e)
    return vinyl

@app.post("/vinyls/", response_model = VinylOut, status_code = status.HTTP_201_CREATED)
def create_vinyl_route(vinyl: VinylCreate, db: Session = Depends(get_db)):
    return create_vinyl(vinyl, db)