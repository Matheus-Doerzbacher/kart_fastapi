from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.configs import settings


class PilotoModel(settings.DBBaseModel):
    __tablename__ = "pilotos"

    id_piloto: int = Column(Integer, primary_key=True)
    nome: str = Column(String(256), nullable=False)
    url_foto: str = Column(String(256), nullable=False)

    # Relacionamentos
    temporada_atual = relationship(
        "TemporadaPilotoModel",
        back_populates="piloto",
        cascade="all, delete-orphan",
        lazy="joined",
        uselist=False,
    )

    resultados = relationship(
        "ResultadoCorridaModel",
        back_populates="piloto",
        cascade="all, delete-orphan",
    )
