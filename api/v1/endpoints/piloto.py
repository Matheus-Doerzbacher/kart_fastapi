from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from core.deps import get_current_user, get_session

from models.__all_models import (
    PilotoModel,
    UsuarioModel,
    TemporadaPilotoModel,
    TemporadaModel,
)
from schemas.piloto_schema import Piloto, PilotoCreate, PilotoUpdate

router = APIRouter(prefix="/pilotos", tags=["pilotos"])


# POST Piloto
@router.post("/", response_model=Piloto, status_code=status.HTTP_201_CREATED)
async def post_piloto(
    piloto: PilotoCreate,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    async with db as session:
        novo_piloto: PilotoModel = PilotoModel(
            nome=piloto.nome,
            url_foto=piloto.url_foto,
        )

        session.add(novo_piloto)
        await session.commit()
        return novo_piloto


@router.get("/temporada/{temporada_id}", response_model=List[Piloto])
async def get_pilotos_por_temporada(
    temporada_id: int,
    db: AsyncSession = Depends(get_session),
):
    async with db as session:
        query = select(TemporadaPilotoModel).filter(
            TemporadaPilotoModel.id_temporada == temporada_id
        )
        result = await session.execute(query)
        pilotos_temporada: List[TemporadaPilotoModel] = result.scalars().unique().all()

        pilotos = []

        for piloto in pilotos_temporada:
            query = select(PilotoModel).filter(
                PilotoModel.id_piloto == piloto.id_piloto
            )
            result = await session.execute(query)
            piloto_model = result.scalars().unique().one_or_none()
            pilotos.append(piloto_model)

        return pilotos


# GET Pilotos
@router.get("/", response_model=List[Piloto])
async def get_pilotos(
    db: AsyncSession = Depends(get_session),
):
    async with db as session:
        query = select(PilotoModel)
        result = await session.execute(query)
        pilotos: List[PilotoModel] = result.scalars().unique().all()

        return pilotos


# GET Piloto por ID
@router.get("/{piloto_id}", response_model=Piloto)
async def get_piloto(
    piloto_id: int,
    db: AsyncSession = Depends(get_session),
):
    async with db as session:
        # Query para buscar o piloto com sua temporada atual
        queryPiloto = select(PilotoModel).filter(PilotoModel.id_piloto == piloto_id)
        result = await session.execute(queryPiloto)
        piloto: PilotoModel = result.scalars().first()

        queryTemporada = select(TemporadaModel).filter(
            TemporadaModel.is_temporada_atual == True
        )
        result = await session.execute(queryTemporada)
        temporada_atual = result.scalars().first()

        if temporada_atual is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não há temporada atual definida",
            )

        queryTemporadaPiloto = select(TemporadaPilotoModel).filter(
            TemporadaPilotoModel.id_piloto == piloto_id,
            TemporadaPilotoModel.id_temporada == temporada_atual.id_temporada,
        )
        result = await session.execute(queryTemporadaPiloto)
        temporada_piloto: TemporadaPilotoModel = result.scalars().first()

        if temporada_piloto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Piloto não encontrado na temporada atual",
            )

        piloto.temporada_atual = temporada_piloto

        return piloto


# PUT Piloto
@router.put("/{piloto_id}", response_model=Piloto)
async def put_piloto(
    piloto_id: int,
    piloto: PilotoUpdate,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    async with db as session:
        query = select(PilotoModel).filter(PilotoModel.id_piloto == piloto_id)
        result = await session.execute(query)
        piloto_bd: PilotoModel = result.scalars().unique().one_or_none()

        if piloto_bd is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Piloto não encontrado",
            )

        if piloto.nome:
            piloto_bd.nome = piloto.nome
        if piloto.url_foto:
            piloto_bd.url_foto = piloto.url_foto

        await session.commit()
        return piloto_bd


# DELETE Piloto
@router.delete("/{piloto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_piloto(
    piloto_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    async with db as session:
        query = select(PilotoModel).filter(PilotoModel.id_piloto == piloto_id)
        result = await session.execute(query)
        piloto_bd: PilotoModel = result.scalars().unique().one_or_none()

        if piloto_bd is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Piloto não encontrado",
            )

        await session.delete(piloto_bd)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
