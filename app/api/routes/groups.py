from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models.group import Group, GroupCreate, GroupUpdate
from app.core.database import get_db

router = APIRouter(prefix="/groups", tags=["groups"])

@router.post("/", response_model=Group)
async def create_group(
    group: GroupCreate, 
    db: AsyncSession = Depends(get_db)
):
    db_group = Group(**group.model_dump())
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return db_group

@router.get("/{group_id}", response_model=Group)
async def read_group(group_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalars().first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.get("/", response_model=List[Group])
async def read_groups(
    skip: int = 0, 
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Group).offset(skip).limit(limit))
    return result.scalars().all()

@router.delete("/{group_id}")
async def delete_group(group_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Group).where(Group.id == group_id))
    group = result.scalars().first()
    
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if len(group.students) > 0:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete group with students"
        )
    
    await db.delete(group)
    await db.commit()
    return {"ok": True}