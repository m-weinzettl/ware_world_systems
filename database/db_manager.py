import psycopg2
from model.shopping_cart.shopping_cart import Shopping_Cart

class DB_Manager:
    def __init__(self):
        self.params = {
            "dbname": "ware_welt_db",
            "user": "postgres",
            "password": "",
            "host": "localhost"
        }

    def save_entity(self, entity):
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    for query, data in entity.get_save_queries():
                        cursor.execute(query, data)
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Fehler beim Speichern: {e}!")

    def load_entities(self, entity_class):
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(entity_class.get_load_query())
                    rows = cursor.fetchall()
                    return [entity_class(*row) for row in rows]
        except psycopg2.Error as e:
            print(f"Fehler beim Laden: {e}!")

    def search_entities(self, entity_class, column, search_term):
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    query = f"{entity_class.get_load_query()} WHERE {column} ILIKE %s"

                    params = (f"%{search_term}%",)

                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    return [entity_class(*row) for row in rows]
        except psycopg2.Error as e:
            print(f"Fehler bei der Suche: {e}!")
            return []

    def save_order(self, cart: Shopping_Cart):
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    query = cart.save_invoice_query()
                    data = (
                        str(cart.customer.customer_id),
                        cart.get_total_price(),
                        cart.generate_invoice_data(),
                        cart.is_company
                    )
                    cursor.execute(query, data)

                    cursor.execute(
                        "DELETE FROM shopping_cart WHERE customer_id = %s",
                        (str(cart.customer.customer_id),)
                    )
                    conn.commit()
                    print("Bestellung erfolgreich archiviert und Warenkorb geleert!")
        except psycopg2.Error as e:
            print(f"Fehler beim Speichern der Order: {e}!")
