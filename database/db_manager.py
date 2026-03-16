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
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                for query, data in entity.get_save_queries():
                    cursor.execute(query, data)

    def load_entities(self, entity_class):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(entity_class.get_load_query())
                rows = cursor.fetchall()
                return [entity_class(*row) for row in rows]