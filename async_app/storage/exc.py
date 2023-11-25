class StorageException(Exception):
    pass


class StoragePermissionDenied(StorageException):
    pass


class InvalidPathError(StorageException):
    pass


class PathNotExistsError(StorageException):
    pass


class NotFileError(StorageException):
    pass


class NotFolderError(StorageException):
    pass


class FolderNotEmptyException(StorageException):
    pass
