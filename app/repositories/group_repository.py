from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.group import Group
from app.models.student import Student


class GroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_group(self, group_data: dict) -> Group:
        group = Group(**group_data)
        self.db.add(group)
        await self.db.commit()
        await self.db.refresh(group)
        return group

    async def get_group(self, group_id: int) -> Group | None:
        result = await self.db.execute(select(Group).where(Group.id == group_id))
        return result.scalars().first()

    async def get_all_groups(self, skip=0, limit=100) -> list[Group]:
        result = await self.db.execute(select(Group).offset(skip).limit(limit))
        return result.scalars().all()

    async def delete_group(self, group: Group):
        await self.db.delete(group)
        await self.db.commit()

    async def get_students_count(self, group_id: int) -> int:
        result = await self.db.execute(
            select(func.count()).where(Student.group_id == group_id)
        )
        return result.scalar()