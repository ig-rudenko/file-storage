from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Имя файла базы данных SQLite
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


# Получение текущей асинхронной сессии базы данных
async def get_async_db():
    async with SessionLocal() as session:
        yield session
