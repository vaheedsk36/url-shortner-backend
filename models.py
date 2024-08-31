# from sqlalchemy import Column, String, Integer, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# class URL(Base):
#     __tablename__ = "urls"
#     id = Column(Integer, primary_key=True, index=True)
#     short_url = Column(String, unique=True, index=True)
#     original_url = Column(String)

# Base.metadata.create_all(bind=engine)
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import os

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = AsyncIOMotorClient(DATABASE_URL)
database = client[DATABASE_NAME]
url_collection = database["urls"]

class URL(BaseModel):
    short_url: str
    original_url: str
