from shared.models.products import Product
from shared.core.config import get_settings
from connection import es


settings = get_settings()


async def load_to_elasticsearch(products: list[Product]):
    for product in products:
        await es.index(
            index=settings.SEARCH_SERVICE_INDEX_NAME,
            id=product.product_id,
            document=product.model_dump()
        )