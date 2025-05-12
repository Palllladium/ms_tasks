from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db_config import engine, redis
from app.routes import auth, users
from sqlmodel import SQLModel
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    
    await redis.ping()
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}