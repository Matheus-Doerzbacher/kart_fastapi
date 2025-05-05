from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from core.deps import get_session, get_current_user
from schemas.temporada_schema import Temporada, TemporadaCreate, TemporadaUpdate
from schemas.piloto_schema import Piloto

from models.__all_models import (
    TemporadaModel,
    UsuarioModel,
    CorridaModel,
    PilotoModel,
    ResultadoCorridaModel,
)

router = APIRouter(prefix="/temporadas", tags=["temporadas"])


# POST Temporada
@router.post("/", response_model=Temporada, status_code=status.HTTP_201_CREATED)
async def create_temporada(
    temporada: TemporadaCreate,
    db: AsyncSession = Depends(get_session),
):
    async with db as session:
        db_temporada = TemporadaModel(**temporada.model_dump())
        session.add(db_temporada)
        await session.commit()
        await session.refresh(db_temporada)
        return db_temporada


# GET Participantes de uma temporada
@router.get("/{temporada_id}/participantes", response_model=int)
async def get_participantes_temporada(
    temporada_id: int,
    db: AsyncSession = Depends(get_session),
):
    async with db as session:
        query = select(CorridaModel).filter(CorridaModel.id_temporada == temporada_id)
        result = await session.execute(query)
        corridas: List[CorridaModel] = result.scalars().all()

        participantes = 0

        for corrida in corridas:
            query = select(ResultadoCorridaModel).filter(
                ResultadoCorridaModel.id_corrida == corrida.id_corrida
            )
            result = await session.execute(query)
            resultado: List[ResultadoCorridaModel] = result.scalars().all()
            participantes += len(resultado)

        return participantes


# GET Temporadas
@router.get("/", response_model=List[Temporada])
async def get_temporadas(
    db: AsyncSession = Depends(get_session),
):
    """
    Retorna todas as temporadas
    """
    async with db as session:
        query = select(TemporadaModel)
        result = await session.execute(query)
        temporadas = result.scalars().all()
        return temporadas


# GET Temporada atual
@router.get("/atual", response_model=Temporada)
async def get_temporada_atual(
    db: AsyncSession = Depends(get_session),
):
    async with db as session:
        query = select(TemporadaModel).filter(TemporadaModel.is_temporada_atual == True)
        result = await session.execute(query)
        temporada = result.scalars().first()

        if temporada is None:
            raise HTTPException(status_code=404, detail="Temporada não encontrada")
        return temporada


# GET Temporada por ID
@router.get("/{temporada_id}", response_model=Temporada)
async def get_temporada(
    temporada_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Retorna uma temporada específica pelo ID
    """
    async with db as session:
        query = select(TemporadaModel).filter(TemporadaModel.id == temporada_id)
        result = await session.execute(query)
        temporada = result.scalars().first()

        if temporada is None:
            raise HTTPException(status_code=404, detail="Temporada não encontrada")
        return temporada


# PUT Temporada
@router.put("/{temporada_id}", response_model=Temporada)
async def update_temporada(
    temporada_id: int,
    temporada: TemporadaUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Atualiza uma temporada específica
    """
    async with db as session:
        query = select(TemporadaModel).filter(TemporadaModel.id == temporada_id)
        result = await session.execute(query)
        db_temporada = result.scalars().first()

        if db_temporada is None:
            raise HTTPException(status_code=404, detail="Temporada não encontrada")

        for key, value in temporada.model_dump(exclude_unset=True).items():
            setattr(db_temporada, key, value)

        await session.commit()
        await session.refresh(db_temporada)
        return db_temporada


# DELETE Temporada
@router.delete("/{temporada_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_temporada(
    temporada_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Remove uma temporada específica
    """
    async with db as session:
        query = select(TemporadaModel).filter(TemporadaModel.id == temporada_id)
        result = await session.execute(query)
        temporada = result.scalars().first()

        if temporada is None:
            raise HTTPException(status_code=404, detail="Temporada não encontrada")

        await session.delete(temporada)
        await session.commit()
        return None
