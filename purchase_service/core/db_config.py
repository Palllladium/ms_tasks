from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from core.config import get_settings


POSTGRES_URL = get_settings().postgres_url
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