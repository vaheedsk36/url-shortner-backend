from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import string
import random
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging
import uvicorn
from logging_config import setup_logging

# Load environment variables from .env file
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

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
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(characters, k=6))
    return short_url

class URLRequest(BaseModel):
    original_url: str
    ssid: str

@app.get("/health-check/")
async def health_test():
    return {"status": "ok"}

@app.post("/shorten/")
async def shorten_url(request: URLRequest):
    short_url = generate_short_url()
    new_url = {"short_url": short_url, "original_url": request.original_url, "ssid": request.ssid}
    await url_collection.insert_one(new_url)
    logger.info(f"Shortened URL: {request.original_url} to {short_url}")
    return {"short_url": short_url}

@app.get("/myurls")
async def get_items(
    ssid: str = Query(None, description="SSID of the URL")
):
    mongo_query = {}

    if ssid:
        mongo_query["ssid"] = {"$regex": ssid, "$options": "i"}  # Case-insensitive search

    # Query the MongoDB collection
    cursor = url_collection.find(mongo_query)

    # Convert cursor to list
    items = await cursor.to_list(length=100)  # Limit to 100 items for performance

    # Convert ObjectId to string for JSON serialization
    for item in items:
        item["_id"] = str(item["_id"])

    # Print the retrieved items to the console
    print(items)  # This will print in the server log where the FastAPI app is running

    # Return the list of items
    return items

@app.get("/{short_url}")
async def redirect_to_url(short_url: str):
    db_url = await url_collection.find_one({"short_url": short_url})
    if db_url is None:
        logger.warning(f"URL not found for short URL: {short_url}")
        raise HTTPException(status_code=404, detail="URL not found")
    
    original_url = db_url["original_url"]
    logger.info(f"Redirecting short URL: {short_url} to {original_url}")
    
    # Use RedirectResponse to redirect to the original URL
    return RedirectResponse(url=original_url)

if __name__ == "__main__":
    logger.info("Starting FastAPI application...")
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT") or 8000), reload=True)
