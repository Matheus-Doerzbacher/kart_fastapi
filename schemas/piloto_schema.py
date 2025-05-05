from pydantic import BaseModel, EmailStr
from typing import Optional

from schemas.temporada_piloto_schema import TemporadaPiloto


class PilotoBase(BaseModel):
    nome: str
    url_foto: Optional[str] = None
    temporada_atual: Optional[TemporadaPiloto]


class PilotoCreate(PilotoBase):
    pass


class PilotoUpdate(PilotoBase):
    nome: Optional[str] = None
    url_foto: Optional[str] = None


class PilotoInDB(PilotoBase):
    id_piloto: int

    class Config:
        from_attributes = True


class Piloto(PilotoInDB):
    pass
