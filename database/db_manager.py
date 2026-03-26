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

    def save_entity(self, entity, password=None):
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    # Holt die Liste der Queries (0: customer, 1: private/company)
                    queries = entity.get_save_queries(password)

                    cust_query, cust_data = queries[0]
                    if "RETURNING" not in cust_query.upper():
                        cust_query += " RETURNING customer_id"

                    cursor.execute(cust_query, cust_data)
                    generated_id = cursor.fetchone()[0]  # Hier ist die neue UUID!

                    # 2. Untertabelle mit der ECHTEN ID füttern
                    sub_query, sub_data = queries[1]

                    # Wir wandeln das Tuple in eine Liste um, um den ersten Wert (None)
                    # durch die generierte ID zu ersetzen
                    final_sub_data = list(sub_data)
                    final_sub_data[0] = generated_id

                    cursor.execute(sub_query, tuple(final_sub_data))

                    conn.commit()
                    print(f"DEBUG: Registrierung erfolgreich für ID {generated_id}")
        except psycopg2.Error as e:
            print(f"Fehler beim Speichern: {e}!")
            if conn:
                conn.rollback()

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
                    query = f"{entity_class.get_load_query()} WHERE {column} = %s"

                    cursor.execute(query, (search_term,))
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

    def check_login(self, mail, password):
        from werkzeug.security import check_password_hash
        from model.customer.customer import Customer
        from model.customer.private_customer import Private_Customer
        from model.customer.company_customer import Company_Customer

        login_query = Customer.login_query()
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(login_query, (mail,))
                    row = cursor.fetchone()

                    if row:
                        # Index 8 ist das Passwort laut deinem SQL
                        hashed_pw_from_db = row[8]

                        if check_password_hash(hashed_pw_from_db, password):
                            # Fallunterscheidung: Firma oder Privat?
                            # row[7] ist die UID (Company), row[5] ist Geb_Date (Privat)

                            if row[7]:  # Wenn eine UID existiert -> Company
                                return Company_Customer(
                                    customer_id=row[0],
                                    mail=row[1],
                                    tel_number=row[2],
                                    name=row[6],  # company_name
                                    address=row[3],
                                    uid=row[7]
                                )
                            else:  # Ansonsten -> Private
                                return Private_Customer(
                                    customer_id=row[0],
                                    mail=row[1],
                                    tel_number=row[2],
                                    name=row[4],  # p.name
                                    address=row[3],
                                    geb_date=row[5]
                                )
            return None
        except psycopg2.Error as e:
            print(f"Login-Fehler: {e}")
            return None

    def get_cart_items(self, customer_id):
        from model.product.book import Book
        from model.product.clothes import Clothes
        from model.product.electronic import Electronic
        from model.shopping_cart.shopping_cart import Shopping_Cart
        load_cart_items = Shopping_Cart.load_cart_items()

        items = []
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(load_cart_items, (str(customer_id),))
                    product_ids = [row[0] for row in cursor.fetchall()]

                    for product_id in product_ids:
                        cursor.execute(Book.get_load_query() + " WHERE p.product_id = %s", (str(product_id),))
                        res = cursor.fetchone()
                        if res:
                            items.append(Book(*res))
                            continue

                        cursor.execute(Electronic.get_load_query() + " WHERE p.id = %s", (str(product_id),))
                        res = cursor.fetchone()
                        if res:
                            items.append(Electronic(*res))
                            continue

                        cursor.execute(Clothes.get_load_query() + " WHERE p.id = %s", (str(product_id),))
                        res = cursor.fetchone()
                        if res:
                            items.append(Clothes(*res))
                            continue

            return items
        except psycopg2.Error as err:
            print(f"Fehler beim Laden des Warenkorbs: {err}")
            return []