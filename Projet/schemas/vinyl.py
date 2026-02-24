from pydantic import BaseModel, ConfigDict  # classe spéciale pour imposer et contrôler les types des données (entre autres)
from typing import Union
from datetime import datetime



class VinylCreate(BaseModel):
    title: str
    artist: str
    year: int | None
    genre: str | None



class VinylOut(BaseModel):
    id: int
    title: str
    artist: str
    year: int | None
    genre: str | None
    added_at: datetime
    model_config = ConfigDict(from_attributes=True) # autorise à lire un objet Python comme source de données
                                                    # sinon Pydantic cherche un dictionnaire



