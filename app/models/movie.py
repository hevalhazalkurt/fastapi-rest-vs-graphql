from typing import List

from sqlalchemy import Integer, ForeignKey, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseDBModel
from app.models.mixins import UUIDMixin



class Movie(BaseDBModel, UUIDMixin):
    title: Mapped[str] = mapped_column(String, index=True)
    release_year: Mapped[int] = mapped_column(Integer)

    director_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('director.uuid'))

    director: Mapped["Director"] = relationship(back_populates="movies")
    genres: Mapped[List["Genre"]] = relationship(
        secondary="moviegenreassociation", back_populates="movies"
    )