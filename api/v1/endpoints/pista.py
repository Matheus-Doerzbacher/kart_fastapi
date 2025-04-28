from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from core.deps import get_session, get_current_user
from models.pista_model import PistaModel
from models.usuario_model import UsuarioModel
from schemas.pista_schema import Pista, PistaCreate, PistaUpdate


router = APIRouter(prefix="/pistas", tags=["pistas"])


# POST Pista
@router.post("/", response_model=Pista, status_code=status.HTTP_201_CREATED)
async def create_pista(
    pista: PistaCreate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    async with db as session:
        db_pista = PistaModel(**pista.model_dump())
        session.add(db_pista)
        await session.commit()
        await session.refresh(db_pista)
        return db_pista


# GET Pistas
@router.get("/", response_model=List[Pista])
async def get_pistas(
    db: AsyncSession = Depends(get_session),
):
    """
    Retorna todas as pistas
    """
    async with db as session:
        query = select(PistaModel)
        result = await session.execute(query)
        pistas = result.scalars().all()
        return pistas


# GET Pista por ID
@router.get("/{pista_id}", response_model=Pista)
async def get_pista(
    pista_id: int,
    db: AsyncSession = Depends(get_session),
):
    """
    Retorna uma pista específica pelo ID
    """
    async with db as session:
        query = select(PistaModel).filter(PistaModel.id == pista_id)
        result = await session.execute(query)
        pista = result.scalars().first()

        if pista is None:
            raise HTTPException(status_code=404, detail="Pista não encontrada")
        return pista


# PUT Pista
@router.put("/{pista_id}", response_model=Pista)
async def update_pista(
    pista_id: int,
    pista: PistaUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Atualiza uma pista específica
    """
    async with db as session:
        query = select(PistaModel).filter(PistaModel.id == pista_id)
        result = await session.execute(query)
        db_pista = result.scalars().first()

        if db_pista is None:
            raise HTTPException(status_code=404, detail="Pista não encontrada")

        for key, value in pista.model_dump(exclude_unset=True).items():
            setattr(db_pista, key, value)

        await session.commit()
        await session.refresh(db_pista)
        return db_pista


# DELETE Pista
@router.delete("/{pista_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pista(
    pista_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Remove uma pista específica
    """
    async with db as session:
        query = select(PistaModel).filter(PistaModel.id == pista_id)
        result = await session.execute(query)
        pista = result.scalars().first()

        if pista is None:
            raise HTTPException(status_code=404, detail="Pista não encontrada")

        await session.delete(pista)
        await session.commit()
        return None
