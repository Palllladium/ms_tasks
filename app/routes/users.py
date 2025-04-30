from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.models.user import User, UserUpdate
from app.models.login import (
    LoginHistory, 
    LoginHistoryOut
)
from app.core.security import (
    get_current_user, 
    get_password_hash
)


router = APIRouter(prefix="/user", tags=["user"])

@router.put("/update", response_model=User)
async def update_user_data(
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновление данных пользователя
    """
    if update_data.email:
        existing_user = await db.execute(
            select(User).where(User.email == update_data.email)
        )
        if existing_user.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = update_data.email
    
    if update_data.password:
        current_user.hashed_password = get_password_hash(update_data.password)
    
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    
    return current_user

@router.get("/history", response_model=List[LoginHistoryOut])
async def get_login_history(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получение истории входов пользователя
    """
    result = await db.execute(
        select(LoginHistory)
        .where(LoginHistory.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(LoginHistory.login_time.desc())
    )
    return result.scalars().all()