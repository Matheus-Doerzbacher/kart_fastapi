from pydantic import BaseModel
from typing import List, Optional


class ResultadoCorridaBase(BaseModel):
    id_corrida: int
    id_piloto: int
    tempo_quali: str
    posicao_quali: int
    posicao_chegada: int
    tempo_melhor_volta: str
    numero_melhor_volta: int
    tempo_piloto_frente: str
    tempo_piloto_lider: str
    voltas: int
    numero_kart: int
    velocidade_media: float


class ResultadoCorridaCreate(ResultadoCorridaBase):
    pass


class ResultadoCorridaUpdate(ResultadoCorridaBase):
    id_corrida: Optional[int] = None
    id_piloto: Optional[int] = None
    tempo_quali: Optional[str] = None
    posicao_quali: Optional[int] = None
    posicao_chegada: Optional[int] = None
    tempo_melhor_volta: Optional[str] = None
    numero_melhor_volta: Optional[int] = None
    tempo_piloto_frente: Optional[str] = None
    tempo_piloto_lider: Optional[str] = None
    voltas: Optional[int] = None
    numero_kart: Optional[int] = None
    velocidade_media: Optional[float] = None


class ResultadoCorridaInDB(ResultadoCorridaBase):
    id_resultado_corrida: int

    class Config:
        from_attributes = True


class ResultadoCorrida(ResultadoCorridaInDB):
    pass
