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
