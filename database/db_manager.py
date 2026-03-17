import psycopg2


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