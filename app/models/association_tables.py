from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseDBModel


class MovieGenreAssociation(BaseDBModel):
    movie_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("movie.uuid", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("genre.uuid", ondelete="CASCADE"), primary_key=True)
