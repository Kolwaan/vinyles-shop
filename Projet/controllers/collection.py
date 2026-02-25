from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from schemas.collection import CollectionCreate
from models.collection import Collection
from models.vinyl import Vinyl
from models.user import User


# CRÉER UNE COLLECTION
def create_collection(collection: CollectionCreate, user: User, db: Session) -> Collection:
    collection_to_create = Collection(
        title=collection.title,
        description=collection.description,
        owner = user
    )
    db.add(collection_to_create)
    db.commit()
    db.refresh(collection_to_create)
    return collection_to_create


# LISTER TOUTES LES COLLECTIONS
def list_collections(skip: int, limit: int, db: Session) -> list[Collection]:
    stmt = select(Collection).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


# RÉCUPÉRER UNE SEULE COLLECTION
def get_collection(collection_id: int, db: Session) -> Collection:
    stmt = select(Collection).where(Collection.id == collection_id).options(joinedload(Collection.vinyls))
    collection = db.execute(stmt).scalars().first()
    if not collection:
        raise Exception("collection not found")
    return collection


# AJOUTER UN VINYL À UNE COLLECTION
def add_vinyl_to_collection(collection_id: int, vinyl_id: int, user: User, db: Session) -> Collection:
    collection = db.get(Collection, collection_id)
    if collection.user_id == user.id:
        vinyl = db.get(Vinyl, vinyl_id)
        if vinyl not in collection.vinyls:
            collection.vinyls.append(vinyl)

        db.commit()
        db.refresh(collection)
    return collection


# RETIRER UN VINYL D'UNE COLLECTION
def remove_vinyl_from_collection(collection_id: int, vinyl_id: int, user: User, db: Session) -> dict:
    collection = db.get(Collection, collection_id)
    if not collection:
        raise Exception(404, "Collection not found")

    if collection.user_id != user.id:
        raise Exception(403, "Not authorized")

    vinyl = db.get(Vinyl, vinyl_id)
    if not vinyl:
        raise Exception(404, "Vinyl not found")

    if vinyl not in collection.vinyls:
        raise Exception(400, "Vinyl not in collection")

    collection.vinyls.remove(vinyl)

    db.commit()
    return {"detail": "Vinyl removed from collection"}