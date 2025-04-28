from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from app.models.group import Group, GroupCreate
from app.models.student import Student
from app.core.database import get_db

router = APIRouter(prefix="/groups", tags=["groups"])

class StudentGroupAction(BaseModel):
    student_id: int

@router.post("/", response_model=Group)
async def create_group(
    group: GroupCreate, 
    db: AsyncSession = Depends(get_db)
):
    db_group = Group(**group.model_dump())
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return db_group

@router.get("/{group_id}", response_model=Group)
async def read_group(group_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalars().first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.get("/", response_model=List[Group])
async def read_groups(
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Group).offset(skip).limit(limit))
    return result.scalars().all()

@router.delete("/{group_id}")
async def delete_group(group_id: int, db: AsyncSession = Depends(get_db)):
    # Проверяем существование группы
    group_result = await db.execute(
        select(Group).where(Group.id == group_id)
    )
    group = group_result.scalars().first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Явно проверяем наличие студентов через запрос
    students_count = await db.execute(
        select(func.count()).where(Student.group_id == group_id)
    )
    count = students_count.scalar()

    if count > 0:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete group with students"
        )

    # Удаляем группу
    await db.delete(group)
    await db.commit()
    
    return {"ok": True}

@router.post("/{group_id}/students", 
    response_model=Student,
    responses={
        404: {"description": "Group or student not found"},
        409: {"description": "Student already in group"}
    }
)
async def add_student_to_group(
    group_id: int,
    student_data: StudentGroupAction,
    db: AsyncSession = Depends(get_db)
):
    # Проверка группы
    group_result = await db.execute(select(Group).where(Group.id == group_id))
    group = group_result.scalars().first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Проверка студента
    student_result = await db.execute(
        select(Student).where(Student.id == student_data.student_id)
    )
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.group_id == group_id:
        raise HTTPException(status_code=409, detail="Student already in group")

    student.group_id = group_id
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student

@router.delete("/{group_id}/students/{student_id}",
    responses={
        404: {"description": "Group or student not found"},
        400: {"description": "Student not in group"}
    }
)
async def remove_student_from_group(
    group_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    group_result = await db.execute(select(Group).where(Group.id == group_id))
    group = group_result.scalars().first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    student_result = await db.execute(select(Student).where(Student.id == student_id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.group_id != group_id:
        raise HTTPException(status_code=400, detail="Student not in group")

    student.group_id = None
    db.add(student)
    await db.commit()
    return {"status": "Student removed from group"}