from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from dotenv import load_dotenv
import os


load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
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