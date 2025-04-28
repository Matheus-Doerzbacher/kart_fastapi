from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from core.configs import settings


class TemporadaModel(settings.DBBaseModel):
    __tablename__ = "temporadas"

    id_temporada: int = Column(Integer, primary_key=True)
    descricao: str = Column(String(256), nullable=False)
    ano: int = Column(Integer, nullable=False)
    is_temporada_atual: bool = Column(Boolean, nullable=False, default=False)

    # Relacionamentos
    corridas = relationship("CorridaModel", back_populates="temporada")
    pilotos = relationship("TemporadaPilotoModel", back_populates="temporada")
