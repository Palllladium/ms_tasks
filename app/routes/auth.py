from fastapi import (
    APIRouter, 
    HTTPException, 
    status, 
    Depends
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from typing import Annotated
from jwt.exceptions import InvalidTokenError

from app.models.user import User, UserCreate
from app.models.login import LoginHistory
from app.core.db_config import get_db, get_redis
from app.auth.utils import hash_password, decode_jwt
from app.core.security import (
    create_access_token,
    create_refresh_token,
    validate_auth_user,
    add_to_redis_blacklist
)


security = HTTPBearer()
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=User)
async def register_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Регистрация нового пользователя.
    """
    existing_user = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing_user.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


@router.post("/login")
async def login_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: User = Depends(validate_auth_user)
):
    """
    Аутентификация пользователя и выдача токенов.\n
    (Вводить только username (это email) и password).
    """  
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)
    
    login_entry = LoginHistory(
        user_id=user.id,
        user_agent=user.email or "Unknown"
    )

    db.add(login_entry)
    await db.commit()
    await db.refresh(login_entry)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
async def update_refresh_token(
    refresh_token: str,
    redis: Redis = Depends(get_redis)
):
    try:
        if await redis.exists(refresh_token):
            raise InvalidTokenError("Token revoked")
        
        payload = decode_jwt(refresh_token)
        if payload.get("type") != "refresh":
            raise InvalidTokenError("Invalid token type")

        new_access_token = create_access_token(payload["sub"])
        await add_to_redis_blacklist(refresh_token, payload["exp"], redis)
    
        return {"access_token": new_access_token}

    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    

@router.post("/logout")
async def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    redis: Redis = Depends(get_redis)
):
    """
    Выход из системы и отзыв refresh token.
    """
    token = credentials.credentials
    if await redis.exists(token):
        raise HTTPException(401, "Token already revoked")

    payload = decode_jwt(token)
    if payload.get("type") != "refresh":
        raise HTTPException(401, "Invalid token type")

    await add_to_redis_blacklist(token, payload["exp"], redis)

    return {"detail": "Logged out successfully"}