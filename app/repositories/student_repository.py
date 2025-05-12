from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import Student
from app.models.group import Group


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_student(self, student_data: dict) -> Student:
        student = Student(**student_data)
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student

    async def get_student(self, student_id: int) -> Student | None:
        result = await self.db.execute(select(Student).where(Student.id == student_id))
        return result.scalars().first()

    async def get_all_students(self, skip=0, limit=100, group_id=None) -> list[Student]:
        query = select(Student)
        if group_id is not None:
            query = query.where(Student.group_id == group_id)
        result = await self.db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def delete_student(self, student: Student):
        await self.db.delete(student)
        await self.db.commit()

    async def get_group(self, group_id: int) -> Group | None:
        result = await self.db.execute(select(Group).where(Group.id == group_id))
        return result.scalars().first()

    async def update_student(self, student: Student, update_data: dict) -> Student:
        for key, value in update_data.items():
            setattr(student, key, value)
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student