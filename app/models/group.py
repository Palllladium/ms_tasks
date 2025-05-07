from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship, Text
from typing import List, Optional
from pydantic import ConfigDict
from sqlalchemy.orm import Mapped, relationship


class GroupBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(sa_type=Text)


class Group(GroupBase, table=True):
    __tablename__ = "groups" # to avoid key word SQL

    id: Optional[int] = Field(default=None, primary_key=True)
    students: Mapped[List["Student"]] = Relationship(
        sa_relationship=relationship(back_populates="group")
    )


class GroupCreate(GroupBase):
    pass


class GroupUpdate(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None