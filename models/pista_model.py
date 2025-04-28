from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.configs import settings


class PistaModel(settings.DBBaseModel):
    __tablename__ = "pistas"

    id_pista: int = Column(Integer, primary_key=True)
    nome: str = Column(String(256), nullable=False)
    url_image: str = Column(String(256), nullable=False)
    local: str = Column(String(256), nullable=False)

    # Relacionamentos
    corridas = relationship("CorridaModel", back_populates="pista")
