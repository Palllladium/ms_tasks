from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from .link import StudentGroupLink

class Group(SQLModel, table=True):
    id:   Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Строковая аннотация "Student"
    students: List["Student"] = Relationship(
        back_populates="groups",
        link_model=StudentGroupLink
    )