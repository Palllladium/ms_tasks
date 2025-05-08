from __future__ import annotations
from sqlmodel import SQLModel, Text, DateTime, Field, Relationship
from typing import Optional
from pydantic import ConfigDict
from sqlalchemy.orm import Mapped, relationship
from datetime import datetime as dt, timezone


class LoginHistoryBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    user_agent: str = Field(sa_type=Text)
    login_time: dt = Field(
        default_factory=lambda: dt.now(timezone.utc),
        sa_type=DateTime(timezone=True)
    )

class LoginHistory(LoginHistoryBase, table=True):
    __tablename__ = "login_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: Mapped[Optional["User"]] = Relationship(
        sa_relationship=relationship(back_populates="login_history")
    )