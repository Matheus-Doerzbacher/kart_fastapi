from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.configs import settings


class ResultadoCorridaModel(settings.DBBaseModel):
    __tablename__ = "resultados_corrida"

    id_resultado_corrida: int = Column(Integer, primary_key=True)
    id_corrida: int = Column(Integer, ForeignKey("corridas.id_corrida"), nullable=False)
    id_piloto: int = Column(Integer, ForeignKey("pilotos.id_piloto"), nullable=False)
    tempo_quali: str = Column(String(256), nullable=False)
    posicao_quali: int = Column(Integer, nullable=False)
    posicao_chegada: int = Column(Integer, nullable=False)
    tempo_melhor_volta: str = Column(String(256), nullable=False)
    numero_melhor_volta: int = Column(Integer, nullable=False)
    tempo_piloto_frente: str = Column(String(256), nullable=False)
    tempo_piloto_lider: str = Column(String(256), nullable=False)
    voltas: int = Column(Integer, nullable=False)
    numero_kart: int = Column(Integer, nullable=False)
    velocidade_media: float = Column(Float, nullable=False)

    # Relacionamentos
    corrida = relationship("CorridaModel", back_populates="resultados")
    piloto = relationship("PilotoModel", back_populates="resultados")
