import httpx
from http import HTTPStatus
from fastapi import HTTPException
from shared.core.config import get_settings


settings = get_settings()
ELASTIC_SEARCH_URL = settings.elastic_search_url
BAD_REQUEST = HTTPStatus.BAD_REQUEST
BAD_GATEWAY = HTTPStatus.BAD_GATEWAY


async def search_products_proxy(name: str | None = None, description: str | None = None) -> list[dict]:
    if not name and not description:
        raise HTTPException(
            status_code=BAD_REQUEST,
            detail="Нужно указать хотя бы одно поле: name или description"
        )

    params = {}
    if name:
        params["name"] = name
    if description:
        params["description"] = description

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(ELASTIC_SEARCH_URL, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=BAD_GATEWAY,
            detail=f"Search service error: {str(e)}"
        )