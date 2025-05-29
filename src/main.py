from typing import List

from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import BookModel, ReaderModel

from fastapi import FastAPI, Depends, Query, status, HTTPException

from src.schemas import (
    BookSchema,
    BookCreateSchema,
    BookUpdateSchema,
    ReaderCreateSchema,
    ReaderSchema,
    ReaderUpdateSchema,
)

app = FastAPI(
    openapi_tags=[
        {"name": "Books", "description": "Операции с книгами"},
        {"name": "Readers", "description": "Операции с читателями"},
    ]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/books",
    response_model=List[BookSchema],
    summary="Получить список всех книг",
    description="Возвращает список всех книг в библиотеке",
    tags=["Books"],
)
async def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(BookModel).offset(skip).limit(limit).all()


@app.get(
    "/books/{book_id}",
    response_model=BookSchema,
    summary="Получить книгу по ID",
    description="Возвращает книгу по ее ID",
    tags=["Books"],
)
async def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )
    return book


@app.post(
    "/books",
    status_code=status.HTTP_201_CREATED,
    response_model=BookSchema,
    summary="Создать новую книгу",
    description="Добавляет новую книгу в библиотеку",
    tags=["Books"],
)
async def create_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.put(
    "/books/{book_id}",
    response_model=BookSchema,
    summary="Обновить книгу",
    description="Обновляет информацию о книге",
    tags=["Books"],
)
async def update_book(
    book_id: int, book: BookUpdateSchema, db: Session = Depends(get_db)
):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить книгу",
    description="Удаляет книгу по её ID",
    tags=["Books"],
)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )
    db.delete(db_book)
    db.commit()
    return


@app.get(
    "/readers",
    response_model=List[ReaderSchema],
    summary="Получить список всех читателей",
    description="Возвращает список всех читателей с пагинацией",
    tags=["Readers"],
)
async def read_readers(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    return db.query(ReaderModel).offset(skip).limit(limit).all()


@app.get(
    "/readers/{reader_id}",
    response_model=ReaderSchema,
    summary="Получить читателя по ID",
    description="Возвращает читателя по его ID",
    tags=["Readers"],
)
async def read_reader(reader_id: int, db: Session = Depends(get_db)):
    reader = db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    if reader is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Читатель не найден"
        )
    return reader


@app.post(
    "/readers",
    response_model=ReaderSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового читателя",
    description="Добавляет нового читателя в библиотеку",
    tags=["Readers"],
)
async def create_reader(
    reader: ReaderCreateSchema, db: Session = Depends(get_db)
):
    db_reader = ReaderModel(**reader.model_dump())
    try:
        db.add(db_reader)
        db.commit()
        db.refresh(db_reader)
        return db_reader
    except Exception as e:
        db.rollback()
        if "uq_reader_email" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Читатель с таким email уже существует",
            )
        raise


@app.put(
    "/readers/{reader_id}",
    response_model=ReaderSchema,
    summary="Обновить читателя",
    description="Обновляет информацию о читателе",
    tags=["Readers"],
)
async def update_reader(
    reader_id: int, reader: ReaderUpdateSchema, db: Session = Depends(get_db)
):
    db_reader = (
        db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    )
    if db_reader is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Читатель не найден"
        )
    for key, value in reader.model_dump(exclude_unset=True).items():
        setattr(db_reader, key, value)
    try:
        db.commit()
        db.refresh(db_reader)
        return db_reader
    except Exception as e:
        db.rollback()
        if "uq_reader_email" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Читатель с таким email уже существует",
            )
        raise


@app.delete(
    "/readers/{reader_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить читателя",
    description="Удаляет читателя по его ID",
    tags=["Readers"],
)
async def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    db_reader = (
        db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    )
    if db_reader is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Читатель не найден"
        )
    db.delete(db_reader)
    db.commit()
    return
