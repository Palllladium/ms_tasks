from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

# Относительные импорты из нашего пакета
from .db.database import init_db, get_session
from .api.student import router as student_router
from .api.group import router as group_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === Startup ===
    init_db()  # создаём таблицы (если нужно)
    yield
    # === Shutdown ===
    # здесь можно закрыть соединения или выполнить другую очистку

# Инициализируем FastAPI с нашим lifespan
app = FastAPI(
    title="Students & Groups API",
    version="1.0.0",
    lifespan=lifespan
)

# Регистрируем роутеры
app.include_router(
    student_router,
    prefix="/students",
    tags=["students"],
    dependencies=[Depends(get_session)]
)
app.include_router(
    group_router,
    prefix="/groups",
    tags=["groups"],
    dependencies=[Depends(get_session)]
)