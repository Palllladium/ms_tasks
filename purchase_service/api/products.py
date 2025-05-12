from http import HTTPStatus
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends, 
    Query
)

from shared.core.db_config import get_db
from shared.models.products import Product

from services.search_proxy import search_products_proxy
from services.products import (
    get_all_products,
    get_product_by_id,
    purchase_product_by_id,
)


router = APIRouter(prefix="/products", tags=["Products"])
NOT_FOUND = HTTPStatus.NOT_FOUND
BAD_REQUEST = HTTPStatus.BAD_REQUEST
BAD_GATEWAY = HTTPStatus.BAD_GATEWAY


@router.get("/", response_model=list[Product])
async def list_products(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Получение списка всех продуктов
    """
    return await get_all_products(db)


@router.get("/search")
async def search_products(
    name: str | None = Query(default=None),
    description: str | None = Query(default=None)
):
    """
    Поиск продуктов по названию или описанию через ElasticSearch
    """
    return await search_products_proxy(name, description)


@router.get("/{product_id}", response_model=Product)
async def get_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int
):
    """
    Получение информации о продукте по ID
    """
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=NOT_FOUND, detail="Продукт не найден")
    return product


@router.post("/purchase/{product_id}")
async def purchase_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_id: int
):
    """
    Покупка продукта по ID
    """
    success = await purchase_product_by_id(db, product_id)
    if not success:
        raise HTTPException(status_code=BAD_REQUEST, detail="Нельзя купить: товара нет в наличии")
    return {"status": "успешно куплено", "product_id": product_id}