import psycopg2
import json
from model.shopping_cart.shopping_cart import Shopping_Cart

class DB_Manager:
    def __init__(self):
        self.params = {
            "dbname": "neondb",
            "user": "neondb_owner",
            "password": "npg_7cGaDp0ToQCt",
            "host": "ep-falling-glitter-ant3xu4o-pooler.c-6.us-east-1.aws.neon.tech",
            "port": 5432,
            "sslmode": "require"
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
                    print(f"DEBUG: {len(rows)} Zeilen gefunden")
                    return [entity_class(*row) for row in rows]
        except psycopg2.Error as e:
            print(f"Fehler beim Laden: {e}!")
            return []

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
        final_price, _ = cart.get_total_price()
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    query = cart.save_invoice_query()
                    data = (
                        str(cart.customer.id),
                        final_price,
                        cart.generate_invoice_data(),
                        cart.is_company
                    )
                    cursor.execute(query, data)

                    # ID aus dem RETURNING-Statement abrufen
                    result = cursor.fetchone()
                    new_order_id = result[0] if result else None
                    # cart nach Kauf löschen
                    cursor.execute(
                        "DELETE FROM shopping_cart WHERE customer_id = %s",
                        (str(cart.customer.id),)
                    )
                    conn.commit()
                    return new_order_id
        except psycopg2.Error as e:
            print(f"Fehler beim Speichern der Order: {e}!")
            return None

    def get_invoice_data(self, order_id):
        query = "SELECT * FROM orders WHERE order_id = %s"
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (str(order_id),))
                    row = cursor.fetchone()

                    if row:
                        data = row[4] if isinstance(row[4], dict) else json.loads(row[4])
                        data['order_id'] = row[0]
                        return data
                    return None
        except psycopg2.Error as e:
            print(f"Fehler beim Laden der Rechnungsdaten: {e}")
            return None

    def check_login(self, email, password):
        query = "SELECT id, name, email FROM customer WHERE email = %s AND password = %s"
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (email, password))
                    row = cursor.fetchone()
                    if row:
                        from model.customer.customer import Customer
                        return Customer(*row)
                    return None
        except psycopg2.Error as e:
            print(f"Login-Fehler: {e}")
            return None