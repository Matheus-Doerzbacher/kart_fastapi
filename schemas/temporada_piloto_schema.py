from pydantic import BaseModel
from typing import List, Optional


class TemporadaPilotoResults(BaseModel):
    pontos: Optional[int] = None
    vitorias: Optional[int] = None
    posicao: Optional[int] = None


class TemporadaPilotoBase(TemporadaPilotoResults):
    id_piloto: int
    id_temporada: int


class TemporadaPilotoCreate(TemporadaPilotoBase):
    pass


class TemporadaPilotoUpdate(TemporadaPilotoBase):
    id_piloto: Optional[int] = None
    id_temporada: Optional[int] = None
    pontos: Optional[int] = None
    vitorias: Optional[int] = None
    posicao: Optional[int] = None


class TemporadaPilotoInDB(TemporadaPilotoBase):
    id_temporada_piloto: int

    class Config:
        from_attributes = True


class TemporadaPiloto(TemporadaPilotoInDB):
    pass
