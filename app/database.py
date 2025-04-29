from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis.asyncio import Redis

from dotenv import load_dotenv
import os


load_dotenv()
DB_URL = os.getenv("DB_URL")
REDIS_URL = os.getenv("REDIS_URL")

engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Взято из проекта с API, добавляем 
# только подключение к Redis

redis = Redis.from_url(REDIS_URL)
def get_redis():
    return redis