from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.db.base_model import BaseDBModel
from app.models.mixins import UUIDMixin


class Director(BaseDBModel, UUIDMixin):
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    movies: Mapped[List["Movie"]] = relationship(back_populates="director")