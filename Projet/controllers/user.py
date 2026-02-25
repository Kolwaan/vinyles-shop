from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate

from utils.hash import hash_password, verify_password


# AJOUTER UN UTILISATEUR
def create_user(user: UserCreate, db: Session) -> User:
    user_to_create = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(user_to_create)
    db.commit()
    db.refresh(user_to_create)
    return user_to_create


# AUTEHTIFICATION
def authenticate(db: Session, username: str, password: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user = db.execute(stmt).scalars().first()

    if not user:
        return None

    if verify_password(user.password, password):
        return user

    return None


# ACCÉDER À UN UTILISATEUR
def get_user(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user = db.execute(stmt).scalars().first()

    if not user:
        return None

    return user