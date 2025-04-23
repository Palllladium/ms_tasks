from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv(encoding="utf-8-sig")

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "postgresql+psycopg2://admin:secret@localhost:5432/studentdb"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    # не уверен, что так будет корректно
    import app.models.link
    import app.models.student
    import app.models.group
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session