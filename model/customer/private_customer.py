from model.customer.customer import Customer

class Private_Customer(Customer):
    def __init__(self, customer_id, mail, tel_number, name, address, geb_date):
        super().__init__(customer_id, mail, tel_number, name, address, geb_date, None)

    @staticmethod
    def get_load_query():
        return """
            SELECT c.customer_id, c.mail, c.tel_number, p.name, c.address, p.geb_date
            FROM customer c
            JOIN private_customer p ON c.customer_id = p.customer_id
        """


    def get_save_queries(self, password):
        # Query 1: Basis-Daten
        query1 = "INSERT INTO public.customer (mail, tel_number, address, password) VALUES (%s, %s, %s, %s) RETURNING customer_id"
        data1 = (self.mail, self.tel_number, self.address, password)

        # Query 2: Private-Daten (ID wird vom DB_Manager gesetzt)
        query2 = "INSERT INTO public.private_customer (customer_id, name, geb_date) VALUES (%s, %s, %s)"
        data2 = (None, self.name, self.geb_date)

        return [(query1, data1), (query2, data2)]