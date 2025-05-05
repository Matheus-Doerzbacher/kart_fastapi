from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CorridaBase(BaseModel):
    data: datetime
    id_pista: int
    id_temporada: int

    class Config:
        json_encoders = {datetime: lambda dt: dt.isoformat()}


class CorridaCreate(CorridaBase):
    pass


class CorridaUpdate(CorridaBase):
    data: Optional[datetime] = None
    id_pista: Optional[int] = None
    id_temporada: Optional[int] = None


class CorridaInDB(CorridaBase):
    id_corrida: int

    class Config:
        from_attributes = True


class Corrida(CorridaInDB):
    pass
