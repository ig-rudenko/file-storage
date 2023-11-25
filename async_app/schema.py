from datetime import datetime

from pydantic import BaseModel, constr, Field


class UserCreate(BaseModel):
    username: constr(max_length=100)
    password: constr(max_length=100)


class User(BaseModel):
    username: str

    class Config:
        from_attributes = True


class TokenPair(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")


class AccessToken(BaseModel):
    access_token: str = Field(..., alias="accessToken")


class RefreshToken(BaseModel):
    refresh_token: str = Field(..., alias="refreshToken")


class File(BaseModel):
    name: str
    size: int
    is_dir: bool = Field(..., alias="isDir")
    mod_time: datetime = Field(..., alias="modTime")

    class Config:
        from_attributes = True


class RenameFile(BaseModel):
    new_name: str = Field(..., alias="newName")
