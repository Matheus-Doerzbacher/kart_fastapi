from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from core.deps import get_session, get_current_user
from models.resultado_corrida_model import ResultadoCorridaModel
from models.usuario_model import UsuarioModel
from schemas.resultado_corrida_schema import (
    ResultadoCorrida,
    ResultadoCorridaCreate,
    ResultadoCorridaUpdate,
)


router = APIRouter(prefix="/resultados-corrida", tags=["resultados-corrida"])


# POST ResultadoCorrida
@router.post("/", response_model=ResultadoCorrida, status_code=status.HTTP_201_CREATED)
async def create_resultado_corrida(
    resultado: ResultadoCorridaCreate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    async with db as session:
        db_resultado = ResultadoCorridaModel(**resultado.model_dump())
        session.add(db_resultado)
        await session.commit()
        await session.refresh(db_resultado)
        return db_resultado


# GET ResultadosCorrida
@router.get("/", response_model=List[ResultadoCorrida])
async def get_resultados_corrida(
    db: AsyncSession = Depends(get_session),
):
    """
    Retorna todos os resultados de corrida
    """
    async with db as session:
        query = select(ResultadoCorridaModel)
        result = await session.execute(query)
        resultados = result.scalars().all()
        return resultados


# GET ResultadoCorrida por ID
@router.get("/{resultado_id}", response_model=ResultadoCorrida)
async def get_resultado_corrida(
    resultado_id: int,
    db: AsyncSession = Depends(get_session),
):
    """
    Retorna um resultado de corrida específico pelo ID
    """
    async with db as session:
        query = select(ResultadoCorridaModel).filter(
            ResultadoCorridaModel.id == resultado_id
        )
        result = await session.execute(query)
        resultado = result.scalars().first()

        if resultado is None:
            raise HTTPException(
                status_code=404, detail="Resultado de corrida não encontrado"
            )
        return resultado


# PUT ResultadoCorrida
@router.put("/{resultado_id}", response_model=ResultadoCorrida)
async def update_resultado_corrida(
    resultado_id: int,
    resultado: ResultadoCorridaUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Atualiza um resultado de corrida específico
    """
    async with db as session:
        query = select(ResultadoCorridaModel).filter(
            ResultadoCorridaModel.id == resultado_id
        )
        result = await session.execute(query)
        db_resultado = result.scalars().first()

        if db_resultado is None:
            raise HTTPException(
                status_code=404, detail="Resultado de corrida não encontrado"
            )

        for key, value in resultado.model_dump(exclude_unset=True).items():
            setattr(db_resultado, key, value)

        await session.commit()
        await session.refresh(db_resultado)
        return db_resultado


# DELETE ResultadoCorrida
@router.delete("/{resultado_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resultado_corrida(
    resultado_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Remove um resultado de corrida específico
    """
    async with db as session:
        query = select(ResultadoCorridaModel).filter(
            ResultadoCorridaModel.id == resultado_id
        )
        result = await session.execute(query)
        resultado = result.scalars().first()

        if resultado is None:
            raise HTTPException(
                status_code=404, detail="Resultado de corrida não encontrado"
            )

        await session.delete(resultado)
        await session.commit()
        return None
