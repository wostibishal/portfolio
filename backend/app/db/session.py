from sqlmodel import  Session
from backend.app.core.config import DATABASE_URL 
from backend.app.db.database import engine



# Dependency function for FastAPI routes
def get_session():
    with Session(engine) as session:
        yield session

