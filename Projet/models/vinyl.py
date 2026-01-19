from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.database import Base

class Vinyl(Base):
    __tablename__ = "vinyls"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    artist = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
