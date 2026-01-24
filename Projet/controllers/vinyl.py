from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas.vinyl import VinylCreate
from models.vinyl import Vinyl


def create_vinyl(vinyl: VinylCreate, db: Session) -> Vinyl:
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

def list_vinyls(skip: int, limit: int, db:Session) -> list[Vinyl]:
    stmt = select(Vinyl).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def get_vinyl(vinyl_id:int, db:Session) -> Vinyl:
    stmt = select(Vinyl).where(Vinyl.id == vinyl_id) 
    vinyl = db.execute(stmt).scalars().first()
    if not vinyl:
        raise Exception("Vinyl not found")
    return vinyl
