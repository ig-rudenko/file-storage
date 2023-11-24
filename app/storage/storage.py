import os
import pathlib
import shutil
from datetime import datetime
from typing import BinaryIO

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
        self._user_storage = STORAGE_PATH / str(user_id)
        self._user_storage.mkdir(parents=True, exist_ok=True)

    @handle_permission_denied
    def list_user_path(self, path: str) -> list[File]:
        self._validate_path(path)
        file_folder = self._user_storage / path

        if file_folder.exists() and not file_folder.is_dir():
            raise NotFolderError(f"`{path}` не является папкой.")
        files = []
        for file in file_folder.glob("*"):
            file_stat = file.stat()
            files.append(
                File(
                    name=file.name,
                    size=file_stat.st_size,
                    isDir=file.is_dir(),
                    modTime=datetime.fromtimestamp(file_stat.st_mtime),
                )
            )
        return files

    @handle_permission_denied
    def create_folder(self, folder_path: str):
        self._validate_path(folder_path)
        (self._user_storage / folder_path).mkdir(parents=True, exist_ok=True)

    @handle_permission_denied
    def upload_file(self, path: str, filename: str, file_obj: BinaryIO):
        self._validate_path(path)
        file_folder = self._user_storage / path
        if file_folder.exists() and not file_folder.is_dir():
            raise NotFolderError(f"`{path}/{filename}` не является папкой.")

        file_folder.mkdir(parents=True, exist_ok=True)

        with (file_folder / filename).open("wb") as f:
            shutil.copyfileobj(file_obj, f, length=1024 * 1024)

    @handle_permission_denied
    def download_file(self, path: str) -> BinaryIO:
        self._validate_path(path)
        file_path = self._user_storage / path
        if not file_path.exists():
            raise PathNotExistsError(f"Файл {path} не найден.")
        if not file_path.is_file():
            raise NotFileError(f"`{path}` не является файлом.")

        return file_path.open("rb")

    @handle_permission_denied
    def delete_file(self, path: str):
        self._validate_path(path)
        file_path = self._user_storage / path
        if not file_path.exists():
            raise PathNotExistsError(f"Файл {path} не найден.")

        if file_path.is_file():
            file_path.unlink(missing_ok=True)
        else:
            try:
                file_path.rmdir()
            except OSError:
                raise FolderNotEmptyException(
                    "Папка должна быть пустой перед удалением."
                )

    @handle_permission_denied
    def rename_file(self, path: str, new_name: str):
        self._validate_path(path)
        file_path = self._user_storage / path
        if not file_path.exists():
            raise FileNotFoundError(f"Файл {path} не найден.")
        file_path.rename(file_path.parent / new_name)

    @staticmethod
    def _validate_path(path: str):
        if not path or ".." in path:
            raise InvalidPathError(f"Неверный путь `{path}`")
