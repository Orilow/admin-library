import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, SessionLocal  # Импортируем SessionLocal
from src.main import app, get_db
from src.models import UserModel, BookModel, ReaderModel
from src.auth import get_password_hash
from unittest.mock import patch

# URL для тестовой базы PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://ilya@localhost:5432/test_library"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)  # Создаём таблицы
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()  # Коммитим изменения
    finally:
        db.rollback()  # Откатываем
        Base.metadata.drop_all(bind=engine)  # Удаляем таблицы

@pytest.fixture(scope="function")
def override_get_db(db):
    def _override_get_db():
        try:
            yield db  # Используем ту же сессию db
        finally:
            pass  # Не закрываем, фикстура db управляет
    return _override_get_db

@pytest.fixture(scope="function")
def client(db, override_get_db):
    # Переопределяем SessionLocal в src.auth
    with patch("src.auth.SessionLocal", TestingSessionLocal):
        # Переопределяем SessionLocal в src.database, если используется
        with patch("src.database.SessionLocal", TestingSessionLocal):
            app.dependency_overrides[get_db] = override_get_db
            yield TestClient(app)
            app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db):
    user = UserModel(
        email="test@library.com",
        password=get_password_hash("testpass")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created test user: {user.email}")
    return user

@pytest.fixture(scope="function")
def test_book(db):
    book = BookModel(
        title="Test Book",
        author="Test Author",
        year_published=2020,
        isbn="1234567890123",
        copies_available=2
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@pytest.fixture(scope="function")
def test_reader(db):
    reader = ReaderModel(
        name="Test Reader",
        email="reader@library.com"
    )
    db.add(reader)
    db.commit()
    db.refresh(reader)
    return reader