import httpx
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter, 
    HTTPException, 
    Depends, 
    Query
)

from core.config import get_settings
from core.db_config import get_db
from models.products import Product
from services.products import (
    get_all_products,
    get_product_by_id,
    purchase_product_by_id,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[Product])
async def list_products(
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Получение списка всех продуктов
    """
    return await get_all_products(db)


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
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


@router.post("/purchase/{product_id}")
async def purchase_product(
    product_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Покупка продукта по ID
    """
    success = await purchase_product_by_id(db, product_id)
    if not success:
        raise HTTPException(status_code=400, detail="Нельзя купить: товара нет в наличии")
    return {"status": "успешно куплено", "product_id": product_id}


@router.get("/search")
async def search_products(
    name: str | None = Query(default=None),
    description: str | None = Query(default=None)
):
    """
    Поиск продуктов по названию или описанию через ElasticSearch
    """
    if not name and not description:
        raise HTTPException(status_code=400, detail="Нужно указать хотя бы одно поле: name или description")

    params = {}
    if name:
        params["name"] = name
    if description:
        params["description"] = description

    ELASTIC_SEARCH_URL = get_settings().elastic_search_url

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(ELASTIC_SEARCH_URL, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Search service error: {str(e)}")