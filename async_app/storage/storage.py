import os
import pathlib
from datetime import datetime
from typing import AsyncIterable

from aiopath import AsyncPath
from fastapi import UploadFile

from .deco import handle_permission_denied
from .exc import (
    NotFileError,
    FolderNotEmptyException,
    NotFolderError,
    InvalidPathError,
    PathNotExistsError,
)
from ..schema import File

STORAGE_PATH = pathlib.Path(__file__).parent.parent.parent / os.getenv(
    "STORAGE_DIR", "user_storage"
)


class UserStorage:
    def __init__(self, user_id: int):
        self._user_id = user_id
        self._user_storage: AsyncPath = AsyncPath(STORAGE_PATH / str(user_id))
        self._user_storage.mkdir(parents=True, exist_ok=True)

    @handle_permission_denied
    async def list_user_path(self, path: str) -> list[File]:
        self._validate_path(path)
        file_folder = self._user_storage / path

        if await file_folder.exists() and not await file_folder.is_dir():
            raise NotFolderError(f"`{path}` не является папкой.")
        files = []
        async for file in file_folder.glob("*"):
            file_stat = await file.stat()
            files.append(
                File(
                    name=file.name,
                    size=file_stat.st_size,
                    isDir=await file.is_dir(),
                    modTime=datetime.fromtimestamp(file_stat.st_mtime),
                )
            )
        return files

    @handle_permission_denied
    async def create_folder(self, folder_path: str):
        self._validate_path(folder_path)
        await (self._user_storage / folder_path).mkdir(parents=True, exist_ok=True)

    @handle_permission_denied
    async def upload_file(self, path: str, file_obj: UploadFile):
        self._validate_path(path)
        file_folder = self._user_storage / path
        file_name = file_obj.filename

        if await file_folder.exists() and not await file_folder.is_dir():
            raise NotFolderError(f"`{path}/{file_name}` не является папкой.")

        await file_folder.mkdir(parents=True, exist_ok=True)

        async with (file_folder / file_name).open("wb") as f:
            while content := await file_obj.read(1024):
                await f.write(content)

    @handle_permission_denied
    async def download_file(self, path: str) -> AsyncIterable[bytes]:
        self._validate_path(path)
        file_path = self._user_storage / path
        if not await file_path.exists():
            raise PathNotExistsError(f"Файл {path} не найден.")
        if not await file_path.is_file():
            raise NotFileError(f"`{path}` не является файлом.")

        async with file_path.open("rb") as f:
            while content := await f.read(1024):
                yield content

    @handle_permission_denied
    async def delete_file(self, path: str):
        self._validate_path(path)
        file_path = self._user_storage / path
        if not await file_path.exists():
            raise PathNotExistsError(f"Файл {path} не найден.")

        if await file_path.is_file():
            await file_path.unlink(missing_ok=True)
        else:
            try:
                await file_path.rmdir()
            except OSError:
                raise FolderNotEmptyException(
                    "Папка должна быть пустой перед удалением."
                )

    @handle_permission_denied
    async def rename_file(self, path: str, new_name: str):
        self._validate_path(path)
        file_path = self._user_storage / path
        if not await file_path.exists():
            raise FileNotFoundError(f"Файл {path} не найден.")
        await file_path.rename(file_path.parent / new_name)

    @staticmethod
    def _validate_path(path: str):
        if not path or ".." in path:
            raise InvalidPathError(f"Неверный путь `{path}`")
