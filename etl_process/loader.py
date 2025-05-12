from shared.models.products import Product
from shared.core.db_config import es, INDEX


async def load_to_elasticsearch(products: list[Product]):
    for product in products:
        await es.index(
            index=INDEX,
            id=product.product_id,
            document=product.model_dump()
        )