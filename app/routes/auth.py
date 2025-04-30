from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status, Header, Depends
from jose import JWTError, jwt
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from typing import Optional

from app.models.user import User, UserCreate
from app.models.login import LoginHistory
from app.core.database import get_db, get_redis
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    SK,
    ALG,
)


router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=User)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрация нового пользователя
    """
    existing_user = await db.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
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
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db),
    user_agent: Optional[str] = Header(default=None),
    redis: Redis = Depends(get_redis)
):
    """
    Аутентификация пользователя и выдача токенов
    """
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    
    login_entry = LoginHistory(
        user_id=user.id,
        user_agent=user_agent or "Unknown"
    )
    db.add(login_entry)
    await db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh_access_token(
    refresh_token: str,
    redis: Redis = Depends(get_redis)
):
    """
    Обновление access token с использованием refresh token
    """
    try:
        payload = jwt.decode(
            refresh_token,
            SK,
            algorithms=[ALG],
            options={"require": ["exp", "sub", "type"]}
        )
        
        if payload.get("type") != "refresh":
            raise JWTError("Invalid token type")
        
        if await redis.exists(refresh_token):
            raise JWTError("Token revoked")
        
        new_access_token = create_access_token({"sub": payload["sub"]})
        return {"access_token": new_access_token, "token_type": "bearer"}
    
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/logout")
async def logout_user(
    refresh_token: str,
    redis: Redis = Depends(get_redis)
):
    """
    Выход из системы и отзыв refresh token
    """
    try:
        payload = jwt.decode(
            refresh_token,
            SK,
            algorithms=[ALG],
            options={"require": ["exp", "sub", "type"]}
        )
        
        expire_timestamp = payload.get("exp")
        current_time = datetime.now(timezone.utc).timestamp()
        ttl = int(expire_timestamp - current_time)
        
        if ttl > 0:
            await redis.set(refresh_token, "revoked", ex=ttl)
        
        return {"detail": "Successfully logged out"}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )