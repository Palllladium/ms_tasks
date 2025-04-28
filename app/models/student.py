from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import ConfigDict
from sqlalchemy.orm import Mapped, relationship


class StudentBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    group_id: Optional[int] = Field(default=None, foreign_key="groups.id")

class Student(StudentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group: Mapped[Optional["Group"]] = Relationship(sa_relationship=relationship(back_populates="students"))

class StudentCreate(StudentBase):
    pass

class StudentUpdate(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    group_id: Optional[int] = None