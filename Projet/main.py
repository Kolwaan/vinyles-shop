from typing import Union

from fastapi import FastAPI, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.database import Base, get_db, engine

from schemas.vinyl import VinylCreate, VinylOut

from controllers.vinyl import create_vinyl, list_vinyls, get_vinyl


app = FastAPI()
Base.metadata.create_all(bind=engine)  # crée les tables dans la BDD, la structure de la BDD.


# ROUTE D'ACCUEIL
@app.get("/")
def read_root():
    return {"Hello": "World"}



# LISTER TOUS LES VINYLS
@app.get("/vinyls")
def list_vinyls_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_vinyls(skip, limit, db)



# RÉCUPÉRER UN SEUL VINYL
@app.get("/vinyls/{vinyl_id}", response_model = VinylOut)
def get_vinyl_route(vinyl_id:int, db: Session = Depends(get_db)):
    try: 
        vinyl = get_vinyl(vinyl_id, db)
    except Exception as e:  # on récupère l'Exception qu'on a créer dans le controller
        raise HTTPException(status_code=404, detail=str(e)) # La route décide comment le communiquer au client (except + HTTPException).
                                                            # e --> message d'erreur dans le controller
    return vinyl


# CRÉER UN VINYL
@app.post("/vinyls/", response_model = VinylOut, status_code = status.HTTP_201_CREATED)

def create_vinyl_route(
    vinyl: VinylCreate,
    db: Session = Depends(get_db)): # FastAPI orchestre le cycle de vie de get_db (injection + fermeture) ;
                                    # SQLAlchemy gère la session BDD                                  
    return create_vinyl(vinyl, db)