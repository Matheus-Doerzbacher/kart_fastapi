from pydantic import BaseModel
from typing import List, Optional


class PistaBase(BaseModel):
    nome: str
    url_image: str
    local: str


class PistaCreate(PistaBase):
    pass


class PistaUpdate(PistaBase):
    nome: Optional[str] = None
    url_image: Optional[str] = None
    local: Optional[str] = None


class PistaInDB(PistaBase):
    id_pista: int

    class Config:
        from_attributes = True


class Pista(PistaInDB):
    pass
