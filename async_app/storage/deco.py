from functools import wraps

from fastapi import HTTPException
from starlette import status

from app.storage.exc import StoragePermissionDenied, PathNotExistsError


def handle_permission_denied(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PermissionError:
            raise StoragePermissionDenied("Permission Denied")
        except (PathNotExistsError, FileNotFoundError):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return wrapper
