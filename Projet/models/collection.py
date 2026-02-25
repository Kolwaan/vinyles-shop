from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from models.database import Base
from sqlalchemy.orm import relationship
from models.collection_vinyl import association_table

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


# many to many
    vinyls = relationship(
        "Vinyl",
        secondary=association_table,
        back_populates="collections"
    )

# one to many
    owner = relationship(
        "User",
        back_populates="collections"
    )