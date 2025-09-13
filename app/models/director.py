from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import BaseDBModel
from app.models.mixins import UUIDMixin


class Director(BaseDBModel, UUIDMixin):
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
