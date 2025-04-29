from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import ConfigDict
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Text

# Модель пользователя
class UserBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    email: str = Field(index=True, unique=True)

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(sa_column=Column(Text))
    login_history: Mapped[List["LoginHistory"]] = Relationship(
        sa_relationship=relationship(back_populates="user")
    )

class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=32,
        examples=["SecurePassword123"],
        description="Пароль должен быть от 8 до 32 символов"
    )

class UserUpdate(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    email: Optional[str] = None
    password: Optional[str] = None