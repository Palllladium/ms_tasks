from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.user import User
from models.login import LoginHistory


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def update_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_login_history(self, user_id: int, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(LoginHistory)
            .where(LoginHistory.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(LoginHistory.login_time.desc())
        )
        return result.scalars().all()