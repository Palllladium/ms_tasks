from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from elasticsearch import AsyncElasticsearch

from shared.core.config import get_settings


settings = get_settings()

engine = create_async_engine(settings.postgres_url, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
es = AsyncElasticsearch(hosts=[settings.elastic_search_url])