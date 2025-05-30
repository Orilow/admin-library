from datetime import datetime, timedelta, timezone
from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from src.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from src.database import SessionLocal
from src.models import BookModel, BorrowedBookModel, ReaderModel, UserModel

from fastapi import FastAPI, Depends, Query, status, HTTPException

from src.schemas import (
    BookSchema,
    BookCreateSchema,
    BookUpdateSchema,
    BorrowedBookCreateSchema,
    BorrowedBookReturnSchema,
    BorrowedBookSchema,
    LoginSchema,
    ReaderCreateSchema,
    ReaderSchema,
    ReaderUpdateSchema,
    TokenSchema,
    UserCreateSchema,
    UserSchema,
)

app = FastAPI(
    openapi_tags=[
        {"name": "Auth", "description": "Аутентификация и регистрация"},
        {
            "name": "Loans",
            "description": "Операции с выдачей и возвратом книг",
        },
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


# Auth endpoints
@app.post(
    "/register",
    response_model=UserSchema,
    status_code=201,
    summary="Зарегистрировать библиотекаря",
    tags=["Auth"],
)
async def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже занят")
    db_user = UserModel(
        email=user.email, password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post(
    "/login",
    response_model=TokenSchema,
    summary="Войти и получить JWT",
    tags=["Auth"],
)
async def login(
    form_data: LoginSchema,
    db: Session = Depends(get_db),
):
    user = (
        db.query(UserModel).filter(UserModel.email == form_data.email).first()
    )
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401, detail="Неверный email или пароль"
        )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Books Enpoints
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
async def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
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
async def create_book(
    book: BookCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
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
    book_id: int,
    book: BookUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
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
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )
    db.delete(db_book)
    db.commit()
    return


# Readers Enpoints
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
    current_user: UserModel = Depends(get_current_user),
):
    return db.query(ReaderModel).offset(skip).limit(limit).all()


@app.get(
    "/readers/{reader_id}",
    response_model=ReaderSchema,
    summary="Получить читателя по ID",
    description="Возвращает читателя по его ID",
    tags=["Readers"],
)
async def read_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    reader = db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    if reader is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Читатель не найден"
        )
    return reader


@app.get(
    "/readers/{reader_id}/borrowed",
    response_model=List[BookSchema],
    summary="Получить список книг, взятых читателем",
    description="Возвращает список всех книг, которые читатель взял и ещё не вернул, включая дублирующиеся экземпляры",
    tags=["Readers", "Loans"],
)
async def read_reader_borrowed(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    reader = db.query(ReaderModel).filter(ReaderModel.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")

    borrowed_entries = (
        db.query(BorrowedBookModel)
        .filter(
            BorrowedBookModel.reader_id == reader_id,
            BorrowedBookModel.return_date.is_(None),
        )
        .options(joinedload(BorrowedBookModel.book))
        .all()
    )

    books = [entry.book for entry in borrowed_entries]

    return books


@app.post(
    "/readers",
    response_model=ReaderSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового читателя",
    description="Добавляет нового читателя в библиотеку",
    tags=["Readers"],
)
async def create_reader(
    reader: ReaderCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
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
    reader_id: int,
    reader: ReaderUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
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
async def delete_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
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


# Loans Endpoints
@app.post(
    "/rent_book",
    response_model=BorrowedBookSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Выдать книгу читателю",
    description="Создаёт запись о выдаче книги с учётом доступности и лимита",
    tags=["Loans"],
)
async def rent_book(
    borrow: BorrowedBookCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    book = db.query(BookModel).filter(BookModel.id == borrow.book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )
    reader = (
        db.query(ReaderModel)
        .filter(ReaderModel.id == borrow.reader_id)
        .first()
    )
    if reader is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Читатель не найден"
        )

    if book.copies_available < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет доступных экземпляров книги",
        )

    active_borrows = (
        db.query(BorrowedBookModel)
        .filter(
            and_(
                BorrowedBookModel.reader_id == borrow.reader_id,
                BorrowedBookModel.return_date.is_(None),
            )
        )
        .count()
    )
    if active_borrows >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Читатель уже взял максимум 3 книги",
        )

    book.copies_available -= 1
    borrowed_book = BorrowedBookModel(
        book_id=borrow.book_id,
        reader_id=borrow.reader_id,
        borrow_date=datetime.now(timezone.utc),
    )
    db.add(borrowed_book)
    db.commit()
    db.refresh(borrowed_book)
    return borrowed_book


@app.post(
    "/return_book",
    response_model=BorrowedBookSchema,
    summary="Вернуть книгу",
    description="Отмечает книгу как возвращённую и увеличивает доступные экземпляры",
    tags=["Loans"],
)
async def return_book(
    borrow: BorrowedBookReturnSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    borrowed_book = (
        db.query(BorrowedBookModel)
        .filter(
            and_(
                BorrowedBookModel.book_id == borrow.book_id,
                BorrowedBookModel.reader_id == borrow.reader_id,
                BorrowedBookModel.return_date.is_(None),
            )
        )
        .first()
    )
    if borrowed_book is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга не была выдана этому читателю или уже возвращена",
        )

    book = db.query(BookModel).filter(BookModel.id == borrow.book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена"
        )

    borrowed_book.return_date = datetime.now(timezone.utc)
    book.copies_available += 1
    db.commit()
    db.refresh(borrowed_book)
    return borrowed_book
