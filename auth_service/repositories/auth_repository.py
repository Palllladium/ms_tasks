from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.user import User
from models.login import LoginHistory


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def add_login_history(self, entry: LoginHistory) -> None:
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry)