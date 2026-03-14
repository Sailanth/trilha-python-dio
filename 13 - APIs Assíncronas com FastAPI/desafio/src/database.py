import databases
import sqlalchemy
from src.config import settings

database = databases.Database(settings.DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL.replace("+aiosqlite", ""),
    connect_args={"check_same_thread": False},
)
