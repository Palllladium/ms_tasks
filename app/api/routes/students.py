from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from app.models.student import (
    Student, 
    StudentCreate, 
    StudentUpdate
)
from app.models.group import Group
from app.core.db_config import get_db


router = APIRouter(prefix="/students", tags=["students"])


class TransferRequest(BaseModel):
    from_group_id: int
    to_group_id: int



@router.post("/", response_model=Student)
async def create_student(
    student: StudentCreate, 
    db: AsyncSession = Depends(get_db)
):
    if student.group_id is not None:
        result = await db.execute(select(Group).where(Group.id == student.group_id))
        if not result.scalars().first():
            raise HTTPException(status_code=400, detail="Invalid group ID")

    db_student = Student(**student.model_dump())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


@router.get("/{student_id}", response_model=Student)
async def read_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/", response_model=List[Student])
async def read_students(
    skip: int = 0,
    limit: int = 100,
    group_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Student)
    if group_id is not None:
        query = query.where(Student.group_id == group_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


@router.patch("/{student_id}", response_model=Student)
async def update_student(
    student_id: int,
    student: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).where(Student.id == student_id))
    db_student = result.scalars().first()
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student.model_dump(exclude_unset=True)
    
    if "group_id" in update_data and update_data["group_id"] is not None:
        group_result = await db.execute(select(Group).where(Group.id == update_data["group_id"]))
        if not group_result.scalars().first():
            raise HTTPException(status_code=400, detail="Invalid group ID")

    for key, value in update_data.items():
        setattr(db_student, key, value)
    
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


@router.delete("/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    await db.delete(student)
    await db.commit()
    return {"ok": True}


@router.post("/{student_id}/transfer",
    responses={
        404: {"description": "Student or group not found"},
        400: {"description": "Student not in source group"},
        409: {"description": "Student already in target group"}
    }
)
async def transfer_student(
    student_id: int,
    transfer_data: TransferRequest,
    db: AsyncSession = Depends(get_db)
):
    student_result = await db.execute(select(Student).where(Student.id == student_id))
    student = student_result.scalars().first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.group_id != transfer_data.from_group_id:
        raise HTTPException(status_code=400, detail="Student not in source group")

    group_result = await db.execute(select(Group).where(Group.id == transfer_data.to_group_id))
    target_group = group_result.scalars().first()
    if not target_group:
        raise HTTPException(status_code=404, detail="Target group not found")

    if student.group_id == transfer_data.to_group_id:
        raise HTTPException(status_code=409, detail="Student already in target group")

    student.group_id = transfer_data.to_group_id
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return {"status": "Student transferred"}