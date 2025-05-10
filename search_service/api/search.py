from fastapi import (
    APIRouter,
    HTTPException,
    Query
)
from http import HTTPStatus
from services.search import search_products


router = APIRouter(prefix="/search", tags=["Search"])
BAD_REQUEST = HTTPStatus.BAD_REQUEST
BAD_GATEWAY = HTTPStatus.BAD_GATEWAY


@router.get("/")
async def search(
    name: str | None = Query(None),
    description: str | None = Query(None)
):
    if not name and not description:
        raise HTTPException(
            status_code=BAD_REQUEST,
            detail="Нужно указать name или description"
        )

    try:
        results = await search_products(name, description)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=BAD_GATEWAY,
            detail=f"Ошибка поиска: {str(e)}"
        )