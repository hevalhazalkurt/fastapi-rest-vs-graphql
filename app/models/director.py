from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseDBModel
from app.models.mixins import UUIDMixin
from app.models.movie import Movie


class Director(BaseDBModel, UUIDMixin):
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    movies: Mapped[list["Movie"]] = relationship(back_populates="director")
