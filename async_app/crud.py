from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schema import UserCreate
from .models import User
from .services.encrypt import encrypt_password


async def get_user(db: AsyncSession, **kwargs) -> User:
    params = [getattr(User, attr) == value for attr, value in kwargs.items()]
    res = await db.execute(select(User).where(*params))
    return res.scalar_one()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    user = User(**user.model_dump())
    user.password = encrypt_password(user.password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
