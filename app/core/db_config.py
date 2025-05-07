from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import SETTINGS


POSTGRES_URL = (
    f"postgresql+asyncpg://"
    f"{SETTINGS.POSTGRES_USER}:{SETTINGS.POSTGRES_PASSWORD}@"
    f"{SETTINGS.POSTGRES_HOST}:{SETTINGS.POSTGRES_PORT}/"
    f"{SETTINGS.POSTGRES_DB}"
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