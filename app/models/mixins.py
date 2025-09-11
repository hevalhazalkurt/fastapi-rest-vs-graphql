from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class UUIDMixin:
    uuid: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True),
        index=True,
        unique=True,
        default=uuid4,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )