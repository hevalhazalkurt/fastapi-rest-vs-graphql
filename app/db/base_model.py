from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseDBModel(DeclarativeBase):
    """
    Base database model
    """
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


