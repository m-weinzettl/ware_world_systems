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

    def save_entity(self, entity, password=None): # password als optionaler Parameter
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    for query, data in entity.get_save_queries(password):
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
                        cart.delete_save_order(),
                        (str(cart.customer.id),)
                    )
                    conn.commit()
                    return new_order_id
        except psycopg2.Error as e:
            print(f"Fehler beim Speichern der Order: {e}!")
            return None

    def get_invoice_data(self, order_id):
        from model.shopping_cart.shopping_cart import Shopping_Cart
        query = Shopping_Cart.get_data_query()
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


#gehört noch in den customer ausgelagert
    def check_login(self, mail, password):
        from werkzeug.security import check_password_hash
        from model.customer.customer import Customer
        # Wir holen uns alle Basis-Daten, um das Objekt korrekt zu befüllen
        login = Customer.login_query()
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(login, (mail,))
                    row = cursor.fetchone()
                    if row:
                        hashed_pw_from_db = row[8]

                        if check_password_hash(hashed_pw_from_db, password):
                            display_name = row[4] if row[4] else row[6]
                            return Customer(
                                customer_id=row[0],
                                mail=row[1],
                                tel_number=row[2],
                                name=display_name,
                                address=row[3],
                                geb_date=row[5],
                                uid=row[7]
                            )

                        # Mapping der DB-Zeile auf deine Customer-Klasse:
                        # row[0]=id, row[1]=mail, row[2]=tel, row[3]=address
                        # row[4]=name_private (p), row[5]=geb_date, row[6]=name_customer (co), row[7]=uid

                         # Privatname oder Firmenname
            return None
        except psycopg2.Error as e:
            print(f"Login-Fehler: {e}")
            return None