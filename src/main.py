from typing import Union

from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import Book

from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/books")
async def read_books(db: Session = Depends(get_db)):
    return db.query(Book).all()