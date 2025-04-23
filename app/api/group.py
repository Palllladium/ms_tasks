from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db.database import get_session
from ..crud.group import (
    create_group, get_group, list_groups, delete_group,
    add_student_to_group, remove_student_from_group, move_student
)
from app.schemas import GroupCreate, GroupRead

router = APIRouter()

@router.post("/", response_model=GroupRead)
def api_create_group(payload: GroupCreate, session: Session = Depends(get_session)):
    return create_group(session, **payload.dict())

@router.get("/{group_id}", response_model=GroupRead)
def api_get_group(group_id: int, session: Session = Depends(get_session)):
    group = get_group(session, group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    return group

@router.get("/", response_model=list[GroupRead])
def api_list_groups(session: Session = Depends(get_session)):
    return list_groups(session)

@router.delete("/{group_id}")
def api_delete_group(group_id: int, session: Session = Depends(get_session)):
    delete_group(session, group_id)
    return {"ok": True}

@router.post("/{group_id}/students/{student_id}")
def api_add_student(group_id: int, student_id: int, session: Session = Depends(get_session)):
    add_student_to_group(session, student_id, group_id)
    return {"ok": True}

@router.delete("/{group_id}/students/{student_id}")
def api_remove_student(group_id: int, student_id: int, session: Session = Depends(get_session)):
    remove_student_from_group(session, student_id, group_id)
    return {"ok": True}

@router.post("/move/")
def api_move_student(from_group_id: int, to_group_id: int, student_id: int, session: Session = Depends(get_session)):
    move_student(session, student_id, from_group_id, to_group_id)
    return {"ok": True}