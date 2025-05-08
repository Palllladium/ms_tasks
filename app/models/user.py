from __future__ import annotations
from sqlmodel import SQLModel, Text, Boolean, Field, Relationship
from typing import Optional, List
from pydantic import ConfigDict
from sqlalchemy.orm import Mapped, relationship


class UserBase(SQLModel):
    model_config = ConfigDict(from_attributes=True)
    email: str = Field(
        index=True, 
        unique=True, 
        sa_type=Text
    )

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(sa_type=Text)
    is_active: bool = Field(sa_type=Boolean, default=True)
    login_history: Mapped[List["LoginHistory"]] = Relationship(
        sa_relationship=relationship(back_populates="user")
    )

class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=6,
        max_length=32,
        description="Пароль должен быть от 6 до 32 символов"
    )

class UserUpdate(SQLModel):
    email: Optional[str] = Field(
        None, 
        description="Новый email (опционально)"
    )
    password: Optional[str] = Field(
        None,
        min_length=6,
        max_length=32,
        description="Новый пароль (опционально)"
    )