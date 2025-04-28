from fastapi import APIRouter

from api.v1.endpoints import (
    corrida,
    piloto,
    pista,
    resultado_corrida,
    temporada_piloto,
    temporada,
    usuario,
)

api_router = APIRouter()

api_router.include_router(corrida.router)
api_router.include_router(piloto.router)
api_router.include_router(pista.router)
api_router.include_router(resultado_corrida.router)
api_router.include_router(temporada_piloto.router)
api_router.include_router(temporada.router)
api_router.include_router(usuario.router)
