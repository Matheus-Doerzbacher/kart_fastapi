from sqlalchemy import Column, Integer, String
from core.configs import settings


class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuarios"

    id_usuario: int = Column(Integer, primary_key=True)
    nome: str = Column(String(256), nullable=False)
    email: str = Column(String(256), nullable=False, unique=True)
    senha: str = Column(String(256), nullable=False)
