from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis.asyncio import Redis

from app.core.config import SETTINGS


POSTGRES_URL = (
    f"postgresql+asyncpg://"
    f"{SETTINGS.POSTGRES_USER}:{SETTINGS.POSTGRES_PASSWORD}@"
    f"{SETTINGS.POSTGRES_HOST}:{SETTINGS.POSTGRES_PORT}/"
    f"{SETTINGS.POSTGRES_DB}"
)

REDIS_URL = (
    f"redis://{SETTINGS.REDIS_HOST}:"
    f"{SETTINGS.REDIS_PORT}/0"
)

engine = create_async_engine(POSTGRES_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

redis = Redis.from_url(REDIS_URL)
def get_redis():
    return redis