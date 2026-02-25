from pydantic import BaseModel, ConfigDict
from datetime import datetime
from schemas.vinyl import VinylOut

class CollectionCreate(BaseModel):
    title: str
    description: str

class CollectionOut(BaseModel):
    id: int
    title: str
    description: str
    added_at: datetime
    vinyls: list[VinylOut]
    model_config = ConfigDict(from_attributes=True) # autorise à lire un objet Python comme source de données
                                                    # sinon Pydantic cherche un dictionnaire
