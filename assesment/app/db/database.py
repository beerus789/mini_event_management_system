from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

DATABASE_URL = "sqlite+aiosqlite:///./event.db"
engine = create_engine("sqlite:///./event.db")

database = Database(DATABASE_URL)
metadata = MetaData()
Base = declarative_base(metadata=metadata)