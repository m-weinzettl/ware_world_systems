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

    search_items = []
    search_items.extend(db.search_entities(Book, "p.name", "Potter"))
    search_items.extend(db.search_entities(Electronic, "p.name", "iPad Pro"))

    new_cart = Shopping_Cart(current_customer)

    for item in search_items:
        new_cart.add_item(item)

    if len(new_cart.items) > 0:
        new_order_id = db.save_order(new_cart)

        if new_order_id:
            print(f"\nBestellung für {current_customer.name} gespeichert!")
            print(f"Gesamtpreis: {new_cart.get_total_price():.2f} EUR")

            invoice_data = db.get_invoice_data(new_order_id)

            pdf_generate = Invoice_To_PDF(invoice_data)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{file_path_bills}Rechnung_{current_customer.name.replace(' ', '_')}_{timestamp}.pdf"

            pdf_generate.create_invoice_to_pdf(file_name)
            print(f"PDF erstellt: {file_name}")
        else:
            print("Fehler beim Speichern der Bestellung.")
    else:
        print("Warenkorb leer. Suche verfeinern!")


if __name__ == "__main__":
    run_local_route()