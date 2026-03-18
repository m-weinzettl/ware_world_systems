import json
import os
from datetime import datetime
from database.db_manager import DB_Manager
from model.customer.private_customer import Private_Customer
from model.product.book import Book
from model.product.clothes import Clothes
from model.product.electronic import Electronic
from model.shopping_cart.shopping_cart import Shopping_Cart
from controller.pdf_generator import Invoice_To_PDF

def run_local_route():
    db = DB_Manager()

    current_customer = Private_Customer("5983c810-5488-4ac4-81b8-1f151c11324a",
                                         "test_3@mail.at",
                                         "0664123123",
                                         "Test Mensch",
                                         "strasse 2 / 8430 Leibnitz",
                                         "2026-12-21")
    file_path_bills = "../bills/"
    os.makedirs(file_path_bills, exist_ok=True)

    all_books = db.load_entities(Book)
    all_clothes = db.load_entities(Clothes)
    all_electronic = db.load_entities(Electronic)

    for book in all_books:
        print(book)
    for cloth in all_clothes:
        print(cloth)
    for electronic in all_electronic:
        print(electronic)

    search_items = []
    search_items.extend(db.search_entities(Book, "p.name", "Potter"))
    search_items.extend(db.search_entities(Book, "b.autor", "Tolkin"))
    search_items.extend(db.search_entities(Electronic, "p.name", "iPad Pro"))

    new_cart = Shopping_Cart(current_customer)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    for item in search_items:
        new_cart.add_item(item)

    if len(new_cart.items) > 0:
        db.save_order(new_cart)
        print(f"\nBestellung für {current_customer.name} gespeichert!")
        print(f"Gesamtpreis: {new_cart.get_total_price():.2f} EUR")

        #pdf generate
        invoice_data = json.loads(new_cart.generate_invoice_data())
        pdf_generate = Invoice_To_PDF()
        pdf_generate.create_invoice_to_pdf(invoice_data, f"{file_path_bills}Rechnung_{current_customer.name.replace(' ', '_')}_{timestamp}.pdf")
    else:
        print("Warenkorb leer. Suche verfeinern!")


  #seach_for_book_title = db.search_entities(Book, "p.name", "Potter")
    #seach_for_book_autor = db.search_entities(Book, "b.autor", "Tolkin")
    #search_for_electronic_brand = db.search_entities(Electronic, "e.brand", "Apple")

  #  print(search_for_electronic_brand, seach_for_book_autor, seach_for_book_title)
if __name__ == "__main__":
    run_local_route()