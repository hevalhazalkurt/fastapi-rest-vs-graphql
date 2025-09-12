from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseDBModel
from app.models.mixins import UUIDMixin


class Genre(BaseDBModel, UUIDMixin):
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    movies: Mapped[List["Movie"]] = relationship(
        secondary="moviegenreassociation", back_populates="genres"
    )