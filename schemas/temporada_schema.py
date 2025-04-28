from pydantic import BaseModel
from typing import List, Optional


class TemporadaBase(BaseModel):
    descricao: str
    ano: int
    is_temporada_atual: bool = False


class TemporadaCreate(TemporadaBase):
    pass


class TemporadaUpdate(TemporadaBase):
    descricao: Optional[str] = None
    ano: Optional[int] = None
    is_temporada_atual: Optional[bool] = None


class TemporadaInDB(TemporadaBase):
    id_temporada: int

    class Config:
        from_attributes = True


class Temporada(TemporadaInDB):
    pass
