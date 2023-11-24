from fastapi import FastAPI
from fastapi.openapi.models import License, Contact
from pydantic_core import Url

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


database.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.router, prefix="/api")
app.include_router(storage.router, prefix="/api")
