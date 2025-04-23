from typing import Optional
from sqlmodel import SQLModel, Field

class StudentGroupLink(SQLModel, table=True):
    student_id: Optional[int] = Field(
        default=None, foreign_key="student.id", primary_key=True
    )
    group_id: Optional[int] = Field(
        default=None, foreign_key="group.id", primary_key=True
    )