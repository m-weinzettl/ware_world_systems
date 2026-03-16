from model.private_customer import Private_Customer
from model.company_customer import Company_Customer
from database.db_manager import DB_Manager

def run_local_route():
    db = DB_Manager()

    print("--- Ware World System (Lokal) ---")
    typ = input("Typ (P für Privat, F für Firma): ").upper()

    # Gemeinsame Daten abfragen
    mail = input("E-Mail: ")
    tel = input("Telefon: ")
    addr = input("Adresse: ")

    try:
        if typ == "P":
            name = input("Name: ")
            geb = input("Geburtsdatum (YYYY-MM-DD): ")

            customer = Private_Customer(mail, tel, name, addr, geb)
            db.save_private_customer(customer)

        elif typ == "F":
            name = input("Firmenname: ")
            uid = input("UID: ")

            customer = Company_Customer(mail, tel, name, addr, uid)
            db.save_company_customer(customer)

        else:
            print("Falscher Typ")
            return

        print(f"\nErfolgreich gespeichert. ID: {customer.id}")
        print(customer)

    except Exception as e:
        print(f"\nFehler im Prozess: {e}")

if __name__ == "__main__":
    run_local_route()