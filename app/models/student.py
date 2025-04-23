from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from .link import StudentGroupLink

class Student(SQLModel, table=True):
    id:   Optional[int] = Field(default=None, primary_key=True)
    name: str
    age:  int

    # Обратите внимание: здесь — строковая аннотация "Group"
    groups: List["Group"] = Relationship(
        back_populates="students",
        link_model=StudentGroupLink
    )