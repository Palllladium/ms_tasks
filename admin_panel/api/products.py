from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends
)
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from typing import Annotated

from shared.models.products import (
    Product, 
    ProductCreate, 
    ProductUpdate
)
from shared.core.db_config import get_db
from services.products import create_product, update_product


router = APIRouter(prefix="/admin/products", tags=["Admin Products"])
NOT_FOUND = HTTPStatus.NOT_FOUND


@router.post("/", response_model=Product)
async def create(
    product: ProductCreate, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Добавление нового продукта
    """
    return await create_product(db, product)


@router.patch("/{product_id}", response_model=Product)
async def update(
    product_id: int, 
    product: ProductUpdate, 
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Обновление существующего продукта
    """
    updated = await update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=NOT_FOUND, detail="Product not found")
    return updated