from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import BookModel


def seed_books():
    db: Session = SessionLocal()
    try:
        if db.query(BookModel).count() > 0:
            print("База уже содержит книги, пропускаем seeding.")
            return

        # Список тестовых книг
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
    except Exception as e:
        db.rollback()
        print(f"Ошибка при добавлении книг: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_books()
