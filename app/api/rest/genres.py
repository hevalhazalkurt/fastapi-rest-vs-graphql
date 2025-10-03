from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.auth.security import get_current_user, require_scope
from app.rest.schemas.genres import GenreCreate, GenreExtended, GenreInDB, GenreUpdate
from app.rest.services.genres import GenresService

router = APIRouter()


@router.get("/")
async def get_all_genres(skip: int = 0, limit: int = 20, service: GenresService = Depends(GenresService), user: dict = Depends(get_current_user)) -> Sequence[GenreInDB]:
    return await service.get_all_genres(skip, limit)


@router.get("/genre")
async def get_genre(
    id: UUID | None = None, name: str | None = None, with_movies: bool = False, service: GenresService = Depends(GenresService), user: dict = Depends(get_current_user)
) -> GenreInDB | GenreExtended:
    if not name and not id:
        raise HTTPException(status_code=404, detail="Genre id or name required")

    if id:
        return await service.get_genre_by_id(id, with_movies)

    assert name
    return await service.get_genre_by_name(name, with_movies)


@router.post("/genre")
async def create_genre(genre_data: GenreCreate, service: GenresService = Depends(GenresService), user: dict = Depends(require_scope(["admin"]))) -> GenreInDB:
    return await service.create_genre(genre_data)


@router.patch("/genre")
async def update_genre(genre_data: GenreUpdate, service: GenresService = Depends(GenresService), user: dict = Depends(require_scope(["admin"]))) -> GenreInDB:
    return await service.update_genre(genre_data)


@router.delete("/genre/{id}")
async def remove_genre(id: UUID, service: GenresService = Depends(GenresService), user: dict = Depends(require_scope(["admin"]))) -> GenreInDB:
    return await service.remove_genre(id)
