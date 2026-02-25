from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    
    
# one to many
    collections = relationship(
    "Collection",
    back_populates="owner", # relation inverse 
    cascade="all"   # quand on supprime un utilisateur on supprime toutes ses collections
)