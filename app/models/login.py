from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import ConfigDict
# from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Text
from datetime import datetime
from time import time

# Модель пользователя
class LoginHistoryBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    user_agent: str = Field(sa_column=Column(Text))
    datetime: datetime = Field(default_factory=time())

class LoginHistory(LoginHistoryBase, table=True):
    __tablename__ = "login_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="login_history") ### ???