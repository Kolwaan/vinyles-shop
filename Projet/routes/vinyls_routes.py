from fastapi import APIRouter, Depends, status

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from models.database import Base, get_db, engine

from schemas.vinyl import VinylCreate, VinylOut

from controllers.vinyl import create_vinyl, list_vinyls, get_vinyl, update_vinyl, delete_vinyl



vinyl_router = APIRouter(prefix='/vinyls', tags = ["Vinyls"])

# ============
# == VINYLS ==
# ============

# LISTER TOUS LES VINYLS
@vinyl_router.get("/")
def list_vinyls_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_vinyls(skip, limit, db)



# RÉCUPÉRER UN SEUL VINYL
@vinyl_router.get("/{vinyl_id}", response_model = VinylOut)
def get_vinyl_route(vinyl_id:int, db: Session = Depends(get_db)):
    try: 
        vinyl = get_vinyl(vinyl_id, db)
    except Exception as e:  # on récupère l'Exception qu'on a créer dans le controller
        raise HTTPException(status_code=404, detail=str(e)) # La route décide comment le communiquer au client (except + HTTPException).
                                                            # e --> message d'erreur dans le controller
    return vinyl


# CRÉER UN VINYL
@vinyl_router.post("/", response_model = VinylOut, status_code = status.HTTP_201_CREATED)

def create_vinyl_route(
    vinyl: VinylCreate,
    db: Session = Depends(get_db)): # FastAPI orchestre le cycle de vie de get_db (injection + fermeture) ;
                                    # SQLAlchemy gère la session BDD                                  
    return create_vinyl(vinyl, db)


# MODIFIER UN VINYL
@vinyl_router.put('/{vinyl_id}', response_model=VinylOut)
def update_vinyl_route(vinyl_id: int, data: VinylCreate, db: Session = Depends(get_db)):
    try:
        vinyl = update_vinyl(vinyl_id, data, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return vinyl


# SUPPRIMER UN VINYL
@vinyl_router.delete('/{vinyl_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_vinyl_route(vinyl_id: int, db: Session = Depends(get_db)):
    try:
        vinyl = delete_vinyl(vinyl_id, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return vinyl
