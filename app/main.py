from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db_config import engine
from app.api.routes import students, groups
from sqlmodel import SQLModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(students.router)
app.include_router(groups.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}