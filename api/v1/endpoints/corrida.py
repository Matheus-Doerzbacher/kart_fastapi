from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from core.deps import get_session, get_current_user
from models.corrida_model import CorridaModel
from models.usuario_model import UsuarioModel
from schemas.corrida_schema import Corrida, CorridaCreate, CorridaUpdate


router = APIRouter(prefix="/corridas", tags=["corridas"])


# POST Corrida
@router.post("/", response_model=Corrida, status_code=status.HTTP_201_CREATED)
async def create_corrida(
    corrida: CorridaCreate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    async with db as session:
        db_corrida = CorridaModel(**corrida.model_dump())
        session.add(db_corrida)
        await session.commit()
        await session.refresh(db_corrida)
        return db_corrida


# GET Corridas por temporada
@router.get("/temporada/{temporada_id}", response_model=List[Corrida])
async def get_corridas_por_temporada(
    temporada_id: int,
    db: AsyncSession = Depends(get_session),
):
    async with db as session:
        query = select(CorridaModel).filter(CorridaModel.id_temporada == temporada_id)
        result = await session.execute(query)
        corridas = result.scalars().all()
        return corridas


# GET Corridas
@router.get("/", response_model=List[Corrida])
async def get_corridas(
    db: AsyncSession = Depends(get_session),
):
    """
    Retorna todas as corridas
    """
    async with db as session:
        query = select(CorridaModel)
        result = await session.execute(query)
        corridas = result.scalars().all()
        return corridas


# GET Corrida por ID
@router.get("/{corrida_id}", response_model=Corrida)
async def get_corrida(
    corrida_id: int,
    db: AsyncSession = Depends(get_session),
):
    """
    Retorna uma corrida específica pelo ID
    """
    async with db as session:
        query = select(CorridaModel).filter(CorridaModel.id == corrida_id)
        result = await session.execute(query)
        corrida = result.scalars().first()

        if corrida is None:
            raise HTTPException(status_code=404, detail="Corrida não encontrada")
        return corrida


# PUT Corrida
@router.put("/{corrida_id}", response_model=Corrida)
async def update_corrida(
    corrida_id: int,
    corrida: CorridaUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Atualiza uma corrida específica
    """
    async with db as session:
        query = select(CorridaModel).filter(CorridaModel.id == corrida_id)
        result = await session.execute(query)
        db_corrida = result.scalars().first()

        if db_corrida is None:
            raise HTTPException(status_code=404, detail="Corrida não encontrada")

        for key, value in corrida.model_dump(exclude_unset=True).items():
            setattr(db_corrida, key, value)

        await session.commit()
        await session.refresh(db_corrida)
        return db_corrida


# DELETE Corrida
@router.delete("/{corrida_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_corrida(
    corrida_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Remove uma corrida específica
    """
    async with db as session:
        query = select(CorridaModel).filter(CorridaModel.id == corrida_id)
        result = await session.execute(query)
        corrida = result.scalars().first()

        if corrida is None:
            raise HTTPException(status_code=404, detail="Corrida não encontrada")

        await session.delete(corrida)
        await session.commit()
        return None
