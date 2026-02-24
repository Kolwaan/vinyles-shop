from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.database import Base   # declarative_base de SQLAlchemy

class Vinyl(Base):  # la classe Vinyl hérite de la classe spéciale Base
    __tablename__ = "vinyls"  # nom donné à la table dans SQL

    id = Column(Integer, primary_key=True, index=True)  # SQLAlchemy, via primary_key=True, dit à la BDD que cette colonne
                                                        # doit se comporter comme une clé primaire (identifiant unique).
                                                        # C'est ensuite PostgreSQL (ou SQLite, etc.) qui génère un nouvel id
                                                        # (avec auto-incrémentation) à chaque insertion (POST).
    title = Column(String, nullable=False, index=True)
    artist = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
