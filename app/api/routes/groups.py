from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pydantic import BaseModel
from http import HTTPStatus

from app.core.db_config import get_db
from app.models.group import Group, GroupCreate
from app.models.student import Student
from app.repositories.group_repository import GroupRepository
from app.repositories.student_repository import StudentRepository


router = APIRouter(prefix="/groups", tags=["groups"])


class StudentGroupAction(BaseModel):
    student_id: int


@router.post("/", response_model=Group)
async def create_group(
    group: GroupCreate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Создание группы
    """
    repo = GroupRepository(db)
    return await repo.create_group(group.model_dump())


@router.get("/{group_id}", response_model=Group)
async def read_group(
    group_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Получение информации о группе по ID
    """
    repo = GroupRepository(db)
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Group not found")
    return group


@router.get("/", response_model=List[Group])
async def read_groups(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """
    Получение информации о всех группах
    """
    repo = GroupRepository(db)
    return await repo.get_all_groups(skip, limit)


@router.delete("/{group_id}")
async def delete_group(
    group_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Удаление группы по ID
    """
    group_repo = GroupRepository(db)
    group = await group_repo.get_group(group_id)

    if not group:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Group not found")

    count = await group_repo.get_students_count(group_id)
    if count > 0:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Cannot delete group with students")

    await group_repo.delete_group(group)
    return {"ok": True}


@router.post("/{group_id}/students", response_model=Student)
async def add_student_to_group(
    group_id: int,
    student_data: StudentGroupAction,
    db: AsyncSession = Depends(get_db)
):
    """
    Добавление студента в группу
    """
    group_repo = GroupRepository(db)
    student_repo = StudentRepository(db)

    group = await group_repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Group not found")

    student = await student_repo.get_student(student_data.student_id)
    if not student:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Student not found")

    if student.group_id == group_id:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Student already in group")

    student.group_id = group_id
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


@router.delete("/{group_id}/students/{student_id}")
async def remove_student_from_group(
    group_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Удаление студента из группы
    """
    group_repo = GroupRepository(db)
    student_repo = StudentRepository(db)

    group = await group_repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Group not found")

    student = await student_repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Student not found")

    if student.group_id != group_id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Student not in group")

    student.group_id = None
    db.add(student)
    await db.commit()
    return {"status": "Student removed from group"}