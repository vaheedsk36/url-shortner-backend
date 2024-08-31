from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import string
import random
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = AsyncIOMotorClient(DATABASE_URL)
database = client[DATABASE_NAME]
url_collection = database["urls"]

def generate_short_url():
    """
    Generates a short URL of a specified length.
    
    Parameters:
    None
    
    Returns:
    str: A short URL of length 6, consisting of random alphanumeric characters.
    """
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(characters, k=6))
    return short_url

# Define a Pydantic model for the request body
class URLRequest(BaseModel):
    original_url: str

@app.get("/health-check/")
async def health_test():
    return {"status": "ok"}

@app.post("/shorten/")
async def shorten_url(request: URLRequest):
    """
    Shortens a given URL by generating a unique short URL and storing it in the database.

    Args:
        request (URLRequest): The request containing the original URL.

    Returns:
        dict: A dictionary containing the generated short URL.
    """
    short_url = generate_short_url()
    new_url = {"short_url": short_url, "original_url": request.original_url}
    await url_collection.insert_one(new_url)
    return {"short_url": short_url}

@app.get("/{short_url}")
async def redirect_to_url(short_url: str):
    """
    Redirects to the original URL based on the provided short URL.

    Args:
    short_url (str): The short URL to redirect from.

    Returns:
    dict: A dictionary containing the original URL.

    Raises:
    HTTPException: If the short URL is not found in the database.
    """
    db_url = await url_collection.find_one({"short_url": short_url})
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": db_url["original_url"]}
