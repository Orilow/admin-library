from sqlalchemy import Column, Integer, String, CheckConstraint

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

    __table_args__ = (
        UniqueConstraint("isbn", name="unique_isbn"),
        CheckConstraint(
            "copies_available >= 0", name="check_copies_available"
        ),
    )
