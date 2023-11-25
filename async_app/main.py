from fastapi import FastAPI

from . import database
from .handlers import auth, storage


app = FastAPI(
    title="Storage App",
    description="Облачное файловое хранилище",
    version="1.0.0",
    contact={
        "name": "ig-rudenko",
        "url": "https://github.com/ig-rudenko",
        "email": "ig.rudenko1@yandex.ru",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


async def create_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()


app.include_router(auth.router, prefix="/api")
app.include_router(storage.router, prefix="/api")
