
from sqlmodel import create_engine
from backend.app.core.config import DATABASE_URL
# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)


