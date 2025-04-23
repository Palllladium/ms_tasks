from sqlmodel import Session, select
from ..models.group import Group, StudentGroupLink

def create_group(session: Session, name: str) -> Group:
    group = Group(name=name)
    session.add(group)
    session.commit()
    session.refresh(group)
    return group

def get_group(session: Session, group_id: int) -> Group | None:
    return session.get(Group, group_id)

def list_groups(session: Session) -> list[Group]:
    return session.exec(select(Group)).all()

def delete_group(session: Session, group_id: int) -> None:
    group = session.get(Group, group_id)
    if group:
        session.delete(group)
        session.commit()

def add_student_to_group(session: Session, student_id: int, group_id: int) -> None:
    link = StudentGroupLink(student_id=student_id, group_id=group_id)
    session.add(link)
    session.commit()

def remove_student_from_group(session: Session, student_id: int, group_id: int) -> None:
    link = session.exec(
        select(StudentGroupLink)
        .where(StudentGroupLink.student_id == student_id)
        .where(StudentGroupLink.group_id == group_id)
    ).one_or_none()
    if link:
        session.delete(link)
        session.commit()

def move_student(session: Session, student_id: int, from_id: int, to_id: int) -> None:
    remove_student_from_group(session, student_id, from_id)
    add_student_to_group(session, student_id, to_id)