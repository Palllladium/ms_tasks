from elasticsearch import AsyncElasticsearch
from core.config import get_settings


settings = get_settings()
index = settings.SEARCH_SERVICE_INDEX_NAME
es = AsyncElasticsearch(hosts=[settings.elastic_search_url])


async def search_products(
    name: str | None = None, 
    description: str | None = None
):
    must_clauses = []

    if name:
        must_clauses.append({"match": {"name": name}})
    if description:
        must_clauses.append({"match": {"description": description}})

    query = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }

    response = await es.search(index=index, body=query)
    return [hit["_source"] for hit in response["hits"]["hits"]]