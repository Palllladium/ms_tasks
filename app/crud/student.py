from sqlmodel import Session, select
#from app.models.student import Student
from ..models.student import Student

def create_student(session: Session, name: str, age: int) -> Student:
    student = Student(name=name, age=age)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def get_student(session: Session, student_id: int) -> Student | None:
    return session.get(Student, student_id)

def list_students(session: Session) -> list[Student]:
    return session.exec(select(Student)).all()

def delete_student(session: Session, student_id: int) -> None:
    student = session.get(Student, student_id)
    if student:
        session.delete(student)
        session.commit()