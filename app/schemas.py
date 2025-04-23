# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel

# ——— Студенты —————————————————————————————————————————————

class StudentCreate(BaseModel):
    name: str
    age: int

class StudentRead(StudentCreate):
    id: int

# ——— Группы ——————————————————————————————————————————————————

class GroupCreate(BaseModel):
    name: str

class GroupRead(GroupCreate):
    id: int