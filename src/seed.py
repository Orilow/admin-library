from datetime import datetime, timedelta, timezone


from src.database import SessionLocal
from src.models import BookModel, ReaderModel, BorrowedBookModel


def seed_books(db):
    if db.query(BookModel).count() > 0:
        print("База уже содержит книги, пропускаем seeding книг.")
        return

    books = [
        {
            "title": "Clean Code",
            "author": "Robert Martin",
            "year_published": 2008,
            "isbn": "9780132350884",
            "copies_available": 3,
        },
        {
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt, David Thomas",
            "year_published": 1999,
            "isbn": "9780201616224",
            "copies_available": 2,
        },
        {
            "title": "Design Patterns",
            "author": "Erich Gamma, Richard Helm",
            "year_published": 1994,
            "isbn": "9780201633610",
            "copies_available": 1,
        },
        {
            "title": "Refactoring",
            "author": "Martin Fowler",
            "year_published": 1999,
            "isbn": "9780201485677",
            "copies_available": 4,
        },
        {
            "title": "You Don't Know JS",
            "author": "Kyle Simpson",
            "year_published": 2015,
            "isbn": "9781491924464",
            "copies_available": 2,
        },
        {
            "title": "The Art of Computer Programming",
            "author": "Donald Knuth",
            "year_published": 1968,
            "isbn": "9780201896831",
            "copies_available": 1,
        },
        {
            "title": "Code Complete",
            "author": "Steve McConnell",
            "year_published": 2004,
            "isbn": "9780735619678",
            "copies_available": 3,
        },
        {
            "title": "Introduction to Algorithms",
            "author": "Thomas H. Cormen",
            "year_published": 2009,
            "isbn": "9780262033848",
            "copies_available": 2,
        },
        {
            "title": "Programming Pearls",
            "author": "Jon Bentley",
            "year_published": 1999,
            "isbn": "9780201657883",
            "copies_available": 1,
        },
        {
            "title": "The Mythical Man-Month",
            "author": "Frederick Brooks",
            "year_published": 1995,
            "isbn": "9780201835953",
            "copies_available": 2,
        },
        {
            "title": "Structure and Interpretation of Computer Programs",
            "author": "Harold Abelson, Gerald Jay Sussman",
            "year_published": 1996,
            "isbn": "9780262510875",
            "copies_available": 1,
        },
        {
            "title": "Head First Design Patterns",
            "author": "Eric Freeman, Elisabeth Robson",
            "year_published": 2004,
            "isbn": "9780596007126",
            "copies_available": 3,
        },
        {
            "title": "Cracking the Coding Interview",
            "author": "Gayle Laakmann McDowell",
            "year_published": 2015,
            "isbn": "9780984782857",
            "copies_available": 2,
        },
        {
            "title": "Effective Java",
            "author": "Joshua Bloch",
            "year_published": 2017,
            "isbn": "9780134685991",
            "copies_available": 1,
        },
        {
            "title": "The Clean Coder",
            "author": "Robert Martin",
            "year_published": 2011,
            "isbn": "9780137081073",
            "copies_available": 2,
        },
    ]

    for book_data in books:
        book = BookModel(**book_data)
        db.add(book)

    db.commit()
    print(f"Добавлено {len(books)} книг в базу.")


def seed_readers(db):
    if db.query(ReaderModel).count() > 0:
        print("База уже содержит читателей, пропускаем seeding читателей.")
        return

    readers = [
        {"name": "John Doe", "email": "john.doe@example.com"},
        {"name": "Jane Smith", "email": "jane.smith@example.com"},
        {"name": "Alice Johnson", "email": "alice.johnson@example.com"},
        {"name": "Bob Brown", "email": "bob.brown@example.com"},
        {"name": "Emma Wilson", "email": "emma.wilson@example.com"},
        {"name": "Michael Chen", "email": "michael.chen@example.com"},
        {"name": "Sarah Davis", "email": "sarah.davis@example.com"},
        {"name": "David Lee", "email": "david.lee@example.com"},
        {"name": "Laura Martinez", "email": "laura.martinez@example.com"},
        {"name": "James Taylor", "email": "james.taylor@example.com"},
        {"name": "Emily Clark", "email": "emily.clark@example.com"},
        {"name": "William Harris", "email": "william.harris@example.com"},
        {"name": "Olivia Lewis", "email": "olivia.lewis@example.com"},
        {"name": "Thomas Walker", "email": "thomas.walker@example.com"},
        {"name": "Sophia Young", "email": "sophia.young@example.com"},
    ]

    for reader_data in readers:
        reader = ReaderModel(**reader_data)
        db.add(reader)

    db.commit()
    print(f"Добавлено {len(readers)} читателей в базу.")


def seed_borrowed_books(db):
    if db.query(BorrowedBookModel).count() > 0:
        print("База уже содержит займы, пропускаем seeding займов.")
        return

    borrows = [
        {
            "book_id": 1,
            "reader_id": 1,
            "borrow_date": datetime.now(timezone.utc) - timedelta(days=10),
            "return_date": None,
        },
        {
            "book_id": 2,
            "reader_id": 1,
            "borrow_date": datetime.now(timezone.utc) - timedelta(days=8),
            "return_date": None,
        },
        {
            "book_id": 3,
            "reader_id": 2,
            "borrow_date": datetime.now(timezone.utc) - timedelta(days=5),
            "return_date": datetime.now(timezone.utc) - timedelta(days=2),
        },
        {
            "book_id": 4,
            "reader_id": 3,
            "borrow_date": datetime.now(timezone.utc) - timedelta(days=7),
            "return_date": None,
        },
        {
            "book_id": 5,
            "reader_id": 4,
            "borrow_date": datetime.now(timezone.utc) - timedelta(days=6),
            "return_date": None,
        },
        {
            "book_id": 6,
            "reader_id": 5,
            "borrow_date": datetime.now(timezone.utc) - timedelta(days=4),
            "return_date": datetime.now(timezone.utc) - timedelta(days=1),
        },
        {
            "book_id": 7,
            "reader_id": 6,
            "borrow_date": datetime.now(timezone.utc) - timedelta(days=3),
            "return_date": None,
        },
        {
            "book_id": 8,
            "reader_id": 7,
            "borrow_date": datetime.now(timezone.utc) - timedelta(days=2),
            "return_date": None,
        },
        {
            "book_id": 9,
            "reader_id": 8,
            "borrow_date": datetime.now(timezone.utc) - timedelta(days=1),
            "return_date": None,
        },
        {
            "book_id": 10,
            "reader_id": 9,
            "borrow_date": datetime.now(timezone.utc),
            "return_date": None,
        },
    ]

    for borrow_data in borrows:
        borrow = BorrowedBookModel(**borrow_data)
        book = (
            db.query(BookModel)
            .filter(BookModel.id == borrow_data["book_id"])
            .first()
        )
        if (
            book
            and book.copies_available > 0
            and borrow_data["return_date"] is None
        ):
            book.copies_available -= 1
        db.add(borrow)

    db.commit()
    print(f"Добавлено {len(borrows)} займов в базу.")


def seed_all():
    db = SessionLocal()
    try:
        seed_books(db)
        seed_readers(db)
        seed_borrowed_books(db)
    except Exception as e:
        db.rollback()
        print(f"Ошибка при seeding: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
