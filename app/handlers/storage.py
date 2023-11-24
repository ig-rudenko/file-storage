from fastapi import APIRouter, Depends, HTTPException, UploadFile
from starlette import status
from starlette.responses import StreamingResponse, Response

from ..models import User
from ..schema import File as FileSchema, RenameFile
from ..services.auth import get_current_user
from ..storage.exc import StorageException
from ..storage.storage import UserStorage

router = APIRouter(tags=["storage"])


@router.get("/items/{path:path}", response_model=list[FileSchema])
def list_items(path: str, user: User = Depends(get_current_user)):
    """Возвращает список папок и файлов"""
    try:
        return UserStorage(user.id).list_user_path(path or ".")
    except StorageException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/items/create-folder/{path:path}", status_code=status.HTTP_201_CREATED)
def create_folder(path: str, user: User = Depends(get_current_user)):
    """Создает новую папку"""
    try:
        UserStorage(user.id).create_folder(path)
        return Response(status_code=status.HTTP_201_CREATED)
    except StorageException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.patch("/item/{path:path}", status_code=status.HTTP_200_OK)
def rename_path(path: str, rename: RenameFile, user: User = Depends(get_current_user)):
    """Переименовывает папку или файл"""
    try:
        UserStorage(user.id).rename_file(path, rename.new_name)
        return Response(status_code=status.HTTP_200_OK)
    except StorageException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/item/{path:path}", status_code=status.HTTP_204_NO_CONTENT)
def delete_path(path: str, user: User = Depends(get_current_user)):
    """Удаляет папку или файл"""
    try:
        UserStorage(user.id).delete_file(path)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except StorageException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/items/upload/{path:path}", status_code=status.HTTP_200_OK)
def upload_files(
    path: str, files: list[UploadFile], user: User = Depends(get_current_user)
):
    """Загружает несколько файлов в указанную папку"""
    try:
        for file in files:
            UserStorage(user.id).upload_file(path or ".", file.filename, file.file)
        return Response(status_code=status.HTTP_200_OK)
    except StorageException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/item/{path:path}")
def download_file(path: str, user: User = Depends(get_current_user)):
    """Скачивает файл"""
    try:
        storage = UserStorage(user.id)
        return StreamingResponse(
            storage.download_file(path), media_type="application/octet-stream"
        )
    except StorageException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
