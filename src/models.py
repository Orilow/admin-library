from sqlalchemy import (
    Column,
    Integer,
    String,
    CheckConstraint,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from src.database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    year_published = Column(Integer, nullable=True)
    isbn = Column(String, nullable=True)
    copies_available = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("isbn", name="uq_isbn"),
        CheckConstraint(
            "copies_available >= 0", name="check_copies_available"
        ),
    )


class ReaderModel(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("email", name="uq_reader_email"),)


class BorrowedBookModel(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    borrow_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)

    book = relationship("BookModel")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
