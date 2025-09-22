from sqlalchemy import UUID, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseDBModel
from app.models.mixins import UUIDMixin


class Movie(BaseDBModel, UUIDMixin):
    title: Mapped[str] = mapped_column(String, index=True)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)

    director_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("director.uuid"), nullable=True)
