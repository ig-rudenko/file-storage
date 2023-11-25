from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from ..schema import UserCreate, TokenPair, AccessToken, RefreshToken
from ..crud import get_user, create_user
from ..database import get_async_db
from ..services.auth import (
    CredentialsException,
    create_jwt_token_pair,
    refresh_access_token,
)
from ..services.encrypt import validate_password

router = APIRouter(prefix="/auth", tags=["auth"])


# Регистрация пользователя
@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """Регистрация нового пользователя"""
    try:
        await get_user(db, username=user.username)
    except exc.NoResultFound:
        await create_user(db, user)
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )


@router.post("/token", response_model=TokenPair)
async def get_tokens(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """Получение пары JWT"""
    try:
        user_model = await get_user(db, username=user.username)
    except exc.NoResultFound:
        raise CredentialsException

    if not validate_password(user.password, user_model.password):
        raise CredentialsException

    access_token, refresh_token = create_jwt_token_pair(user_id=user_model.id)
    return TokenPair(accessToken=access_token, refreshToken=refresh_token)


@router.post("/token/refresh", response_model=AccessToken)
def refresh(token: RefreshToken):
    """Получение нового access token через refresh token"""
    return AccessToken(accessToken=refresh_access_token(token.refresh_token))
