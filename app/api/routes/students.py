from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from http import HTTPStatus

from app.core.db_config import get_db
from app.models.student import Student, StudentCreate, StudentUpdate
from app.repositories.student_repository import StudentRepository
from app.repositories.group_repository import GroupRepository


router = APIRouter(prefix="/students", tags=["students"])


class TransferRequest(BaseModel):
    from_group_id: int
    to_group_id: int


@router.post("/", response_model=Student)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Создание студента
    """
    repo = StudentRepository(db)
    group_repo = GroupRepository(db)

    if student.group_id is not None:
        if not await group_repo.get_group(student.group_id):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid group ID")

    return await repo.create_student(student)


@router.get("/{student_id}", response_model=Student)
async def read_student(
    student_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Получение студента по ID
    """
    repo = StudentRepository(db)
    student = await repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Student not found")
    return student


@router.get("/", response_model=List[Student])
async def read_students(
    skip: int = 0,
    limit: int = 100,
    group_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Получение всех студентов
    """
    repo = StudentRepository(db)
    return await repo.get_students(skip, limit, group_id)


@router.patch("/{student_id}", response_model=Student)
async def update_student(
    student_id: int,
    student: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить информацию о студенте по ID
    """
    repo = StudentRepository(db)
    group_repo = GroupRepository(db)

    update_data = student.model_dump(exclude_unset=True)

    if "group_id" in update_data and update_data["group_id"] is not None:
        if not await group_repo.get_group(update_data["group_id"]):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid group ID")

    updated = await repo.update_student(student_id, update_data)
    if not updated:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Student not found")
    return updated


@router.delete("/{student_id}")
async def delete_student(
    student_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить студента по ID
    """
    repo = StudentRepository(db)
    deleted = await repo.delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Student not found")
    return {"ok": True}


@router.post("/{student_id}/transfer")
async def transfer_student(
    student_id: int,
    transfer_data: TransferRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Перевести студента в другую группу
    """
    student_repo = StudentRepository(db)
    group_repo = GroupRepository(db)

    student = await student_repo.get_student(student_id)
    if not student:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Student not found")

    if student.group_id != transfer_data.from_group_id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Student not in source group")

    if not await group_repo.get_group(transfer_data.to_group_id):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Target group not found")

    if student.group_id == transfer_data.to_group_id:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Student already in target group")

    return await student_repo.transfer_student(student, transfer_data.to_group_id)
