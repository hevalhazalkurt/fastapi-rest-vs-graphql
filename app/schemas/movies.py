from uuid import UUID

from pydantic import ConfigDict

from app.schemas.base_schema import ResponseSchema


class MovieInDB(ResponseSchema):
    uuid: UUID
    title: str
    release_year: int

    model_config = ConfigDict(from_attributes=True)