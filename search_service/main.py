from fastapi import FastAPI
from api.search import router as search_router

app = FastAPI(title="Product Search Service")

app.include_router(search_router)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}