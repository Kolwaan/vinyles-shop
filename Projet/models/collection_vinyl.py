# TABLE PIVOT (relation many to many)

from sqlalchemy import Table, Column, ForeignKey
from models.database import Base

association_table = Table(
    "collection_vinyl",
    Base.metadata,
    Column("collection_id", ForeignKey("collections.id"), primary_key=True),
    Column("vinyl_id", ForeignKey("vinyls.id"), primary_key=True),
)