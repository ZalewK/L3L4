from models import Book, db, BookSchema

class BookService:
    book_schema = BookSchema()
    books_schema = BookSchema(many=True)

    @staticmethod
    def get_all_books(page=1, per_page=10):
        start = (page - 1) * per_page
        end = start + per_page

        all_books = Book.query.all()
        paginated_books = all_books[start:end]

        result = {
            'books': BookService.books_schema.dump(paginated_books),
            'total_pages': len(all_books) // per_page + 1,
            'total_items': len(all_books)
        }
        return result

    @staticmethod
    def get_book_by_id(book_id):
        book = Book.query.get(book_id)
        if book:
            return BookService.book_schema.dump(book)
        else:
            return None

    @staticmethod
    def add_book(title, author):
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        return BookService.book_schema.dump(new_book)

    @staticmethod
    def update_book(book_id, title, author):
        book = Book.query.get(book_id)
        if book:
            book.title = title
            book.author = author
            db.session.commit()
            return BookService.book_schema.dump(book)
        else:
            return None

    @staticmethod
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return BookService.book_schema.dump(book)
        else:
            return None
        
    @staticmethod
    def clear_and_initialize_data():
        db.session.query(Book).delete()

        book1 = Book(title="Antygona", author="Sofokles")
        book2 = Book(title="Ksiega", author="Karol Zalewski")
        book3 = Book(title="Test", author="Tester Test")

        db.session.add(book1)
        db.session.add(book2)
        db.session.add(book3)

        db.session.commit()
