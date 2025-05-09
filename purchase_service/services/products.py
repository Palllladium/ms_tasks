from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Annotated, List
from fastapi import Depends

from core.db_config import get_db
from models.products import Product


async def get_all_products(
        db: Annotated[AsyncSession, Depends(get_db)]
) -> List[Product]:
    """
    Получение списка всех продуктов
    """
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_product_by_id(
        db: Annotated[AsyncSession, Depends(get_db)],
        product_id: int
) -> Product | None:
    """
    Получение одного продукта по ID
    """
    result = await db.execute(select(Product).where(Product.product_id == product_id))
    return result.scalar_one_or_none()


async def purchase_product_by_id(
        db: Annotated[AsyncSession, Depends(get_db)],
        product_id: int
) -> bool:
    """
    Покупка одного продукта по ID
    """
    product = await get_product_by_id(db, product_id)
    if not product or product.count_left <= 0:
        return False
    else:
        product.count_left -= 1
        await db.commit()
        await db.refresh(product)
        return True