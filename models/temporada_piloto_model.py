from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class TemporadaPilotoModel(settings.DBBaseModel):
    __tablename__ = "temporada_pilotos"

    id_temporada_piloto: int = Column(Integer, primary_key=True)
    id_piloto: int = Column(Integer, ForeignKey("pilotos.id_piloto"), nullable=False)
    id_temporada: int = Column(
        Integer,
        ForeignKey("temporadas.id_temporada"),
        nullable=False,
    )
    pontos: int = Column(Integer, nullable=True, default=None)
    vitorias: int = Column(Integer, nullable=True, default=None)
    posicao: int = Column(Integer, nullable=True, default=None)

    # Relacionamentos
    piloto = relationship("PilotoModel", back_populates="temporadas")
    temporada = relationship("TemporadaModel", back_populates="pilotos")
