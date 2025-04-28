from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class CorridaModel(settings.DBBaseModel):
    __tablename__ = "corridas"

    id_corrida: int = Column(Integer, primary_key=True)
    data: DateTime = Column(DateTime, nullable=False)
    id_pista: int = Column(Integer, ForeignKey("pistas.id_pista"), nullable=False)
    id_temporada: int = Column(
        Integer,
        ForeignKey("temporadas.id_temporada"),
        nullable=False,
    )

    # Relacionamentos
    pista = relationship("PistaModel", back_populates="corridas")
    temporada = relationship("TemporadaModel", back_populates="corridas")
    resultados = relationship("ResultadoCorridaModel", back_populates="corrida")
