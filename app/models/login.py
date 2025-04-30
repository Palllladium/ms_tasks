from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import ConfigDict
# from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Text, DateTime
from datetime import datetime as dt, timezone


class LoginHistoryBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    user_agent: str = Field(sa_column=Column(Text))
    login_time: dt = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: dt.now(timezone.utc)
    )

class LoginHistory(LoginHistoryBase, table=True):
    __tablename__ = "login_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="login_history") ### ???

class LoginHistoryOut(LoginHistoryBase):
    model_config = ConfigDict(from_attributes=True)