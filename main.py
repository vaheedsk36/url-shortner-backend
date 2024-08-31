from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel  # Import Pydantic's BaseModel
import string
import random

from models import Base, URL, SessionLocal, engine

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(characters, k=3))
    return short_url

# Define a Pydantic model for the request body
class URLRequest(BaseModel):
    original_url: str

@app.post("/shorten/")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    short_url = generate_short_url()
    db_url = URL(short_url=short_url, original_url=request.original_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {"short_url": short_url}

@app.get("/{short_url}")
def redirect_to_url(short_url: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_url == short_url).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": db_url.original_url}
