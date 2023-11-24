from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from typing_extensions import Annotated

from app.database import Base

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
varchar100 = Annotated[str, mapped_column(String(64))]


# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    username: Mapped[varchar100] = mapped_column(unique=True, nullable=False)
    password: Mapped[varchar100] = mapped_column(nullable=False)
