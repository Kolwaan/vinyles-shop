from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas.vinyl import VinylCreate
from models.vinyl import Vinyl

# CRÉER UN VINYL
def create_vinyl(vinyl: VinylCreate, db: Session) -> Vinyl: # On retourne l'entité (Model) Vinyl
    vinyl_to_create = Vinyl(
        title = vinyl.title,
        artist = vinyl.artist,
        year = vinyl.year,
        
        genre = vinyl.genre
    )
    db.add(vinyl_to_create)     #|
    db.commit()                 #| Session écrit les données dans la BDD
    db.refresh(vinyl_to_create) #|
    return vinyl_to_create


# LISTER TOUS LES VINYLS
def list_vinyls(skip: int, limit: int, db:Session) -> list[Vinyl]:  # On retourne une liste d'entités (Model) Vinyl
    stmt = select(Vinyl).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all() # Session lit les données dans la BDD


# RÉCUPÉRER UN SEUL VINYL
def get_vinyl(vinyl_id:int, db:Session) -> Vinyl:   # On retourne l'entité (Model) Vinyl
    stmt = select(Vinyl).where(Vinyl.id == vinyl_id) 
    vinyl = db.execute(stmt).scalars().first()  # Session lit les données dans la BDD
    if not vinyl:
        raise Exception("Vinyl not found")  # Le controller signale le problème avec raise.
                                            # La route décide comment le communiquer au client (except + HTTPException).
    return vinyl
