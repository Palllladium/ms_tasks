from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db.database import get_session
from ..crud.student import create_student, get_student, list_students, delete_student
from ..schemas import StudentCreate, StudentRead

router = APIRouter()

@router.post("/", response_model=StudentRead)
def api_create_student(
    payload: StudentCreate,
    session: Session = Depends(get_session)
):
    return create_student(session, **payload.dict())

@router.get("/{student_id}", response_model=StudentRead)
def api_get_student(
    student_id: int,
    session: Session = Depends(get_session)
):
    student = get_student(session, student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return student

@router.get("/", response_model=list[StudentRead])
def api_list_students(session: Session = Depends(get_session)):
    return list_students(session)

@router.delete("/{student_id}")
def api_delete_student(
    student_id: int,
    session: Session = Depends(get_session)
):
    delete_student(session, student_id)
    return {"ok": True}