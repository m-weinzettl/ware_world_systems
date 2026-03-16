import psycopg2

class DB_Manager:
    def __init__(self):
        self.params = {
            "dbname": "ware_welt_db",
            "user": "postgres",
            "password": "",
            "host": "localhost"
        }

    def save_private_customer(self, private_customer):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                # basis infos -
                cursor.execute(
                    "INSERT INTO customer (customer_id, mail, tel_number, address) VALUES (%s, %s, %s, %s)",
                    (str(private_customer.id), private_customer.mail, private_customer.tel_number, private_customer.address)
                )
                # private_customer infos
                cursor.execute(
                    "INSERT INTO private_customer (customer_id, name, geb_date) VALUES (%s, %s, %s)",
                    (str(private_customer.id), private_customer.name, private_customer.geb_date)
                )

    def save_company_customer(self, company_customer):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                # basis infos
                cursor.execute(
                    "INSERT INTO customer (customer_id, mail, tel_number, address) VALUES (%s, %s, %s, %s)",
                    (str(company_customer.id), company_customer.mail, company_customer.tel_number, company_customer.address)
                )
                # company_customer infos
                cursor.execute(
                    "INSERT INTO company_customer (customer_id, company_name, uid_number) VALUES (%s, %s, %s)",
                    (str(company_customer.id), company_customer.name, company_customer.uid)
                )