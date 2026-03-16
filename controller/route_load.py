
from database.db_manager import DB_Manager
from database.queries import load_all_books
from model.product import Product
from model.book import Book
from model.clothes import Clothes
from model.electronic import Electronic

def run_local_route():
    db = DB_Manager()

    all_books = db.load_entities(Book)
    all_clothes = db.load_entities(Clothes)
    all_electronic = db.load_entities(Electronic)

    for book in all_books:
        print(book)
    for cloth in all_clothes:
        print(cloth)
    for electronic in all_electronic:
        print(electronic)

if __name__ == "__main__":
    run_local_route()