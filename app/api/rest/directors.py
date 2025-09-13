from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.directors import DirectorInDB, DirectorExtended
from app.services.directors import DirectorsService

router = APIRouter()


@router.get("/")
async def get_all_directors(
        with_movies: bool = False,
        skip: int = 0,
        limit: int = 20,
        service: DirectorsService = Depends(DirectorsService)
) -> Sequence[DirectorInDB | DirectorExtended]:
    return await service.get_all_directors(skip, limit, with_movies)


@router.get("/director")
async def get_director(
        id: UUID | None = None,
        name: str | None = None,
        with_movies: bool = False,
    service: DirectorsService = Depends(DirectorsService)
) -> DirectorInDB | DirectorExtended:
    if not name and not id:
        raise HTTPException(status_code=404, detail="Director id or name required")

    if id:
        return await service.get_director_by_id(id, with_movies)

    assert name
    return await service.get_director_by_name(name, with_movies)



