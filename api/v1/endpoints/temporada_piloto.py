from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from core.deps import get_session, get_current_user
from models.temporada_piloto_model import TemporadaPilotoModel
from models.usuario_model import UsuarioModel
from schemas.temporada_piloto_schema import (
    TemporadaPiloto,
    TemporadaPilotoCreate,
    TemporadaPilotoUpdate,
)


router = APIRouter(prefix="/temporadas-pilotos", tags=["temporadas-pilotos"])


# POST TemporadaPiloto
@router.post("/", response_model=TemporadaPiloto, status_code=status.HTTP_201_CREATED)
async def create_temporada_piloto(
    temporada_piloto: TemporadaPilotoCreate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    async with db as session:
        db_temporada_piloto = TemporadaPilotoModel(**temporada_piloto.model_dump())
        session.add(db_temporada_piloto)
        await session.commit()
        await session.refresh(db_temporada_piloto)
        return db_temporada_piloto


# GET TemporadasPilotos
@router.get("/", response_model=List[TemporadaPiloto])
async def get_temporadas_pilotos(
    db: AsyncSession = Depends(get_session),
):
    """
    Retorna todas as temporadas-pilotos
    """
    async with db as session:
        query = select(TemporadaPilotoModel)
        result = await session.execute(query)
        temporadas_pilotos = result.scalars().all()
        return temporadas_pilotos


# GET TemporadaPiloto por ID
@router.get("/{temporada_piloto_id}", response_model=TemporadaPiloto)
async def get_temporada_piloto(
    temporada_piloto_id: int,
    db: AsyncSession = Depends(get_session),
):
    """
    Retorna uma temporada-piloto específica pelo ID
    """
    async with db as session:
        query = select(TemporadaPilotoModel).filter(
            TemporadaPilotoModel.id_temporada_piloto == temporada_piloto_id
        )
        result = await session.execute(query)
        temporada_piloto = result.scalars().first()

        if temporada_piloto is None:
            raise HTTPException(
                status_code=404, detail="Temporada-piloto não encontrada"
            )
        return temporada_piloto


# PUT TemporadaPiloto
@router.put("/{temporada_piloto_id}", response_model=TemporadaPiloto)
async def update_temporada_piloto(
    temporada_piloto_id: int,
    temporada_piloto: TemporadaPilotoUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Atualiza uma temporada-piloto específica
    """
    async with db as session:
        query = select(TemporadaPilotoModel).filter(
            TemporadaPilotoModel.id_temporada_piloto == temporada_piloto_id
        )
        result = await session.execute(query)
        db_temporada_piloto = result.scalars().first()

        if db_temporada_piloto is None:
            raise HTTPException(
                status_code=404, detail="Temporada-piloto não encontrada"
            )

        for key, value in temporada_piloto.model_dump(exclude_unset=True).items():
            setattr(db_temporada_piloto, key, value)

        await session.commit()
        await session.refresh(db_temporada_piloto)
        return db_temporada_piloto


# DELETE TemporadaPiloto
@router.delete("/{temporada_piloto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_temporada_piloto(
    temporada_piloto_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Remove uma temporada-piloto específica
    """
    async with db as session:
        query = select(TemporadaPilotoModel).filter(
            TemporadaPilotoModel.id_temporada_piloto == temporada_piloto_id
        )
        result = await session.execute(query)
        temporada_piloto = result.scalars().first()

        if temporada_piloto is None:
            raise HTTPException(
                status_code=404, detail="Temporada-piloto não encontrada"
            )

        await session.delete(temporada_piloto)
        await session.commit()
        return None
