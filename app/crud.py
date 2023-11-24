from sqlalchemy import select
from sqlalchemy.orm import Session

from .schema import UserCreate
from .models import User
from .services.encrypt import encrypt_password


def get_user(db: Session, **kwargs) -> User:
    params = [getattr(User, attr) == value for attr, value in kwargs.items()]
    return db.execute(select(User).where(*params)).scalar_one()


def create_user(db: Session, user: UserCreate) -> User:
    user = User(**user.model_dump())
    user.password = encrypt_password(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
