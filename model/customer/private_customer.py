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
        # Holt die Query mit der ID aus der Basisklasse (Customer)
        queries = super().get_save_queries(password)

        # Query 2: Nutzt direkt self.id (statt None), da sie in Python schon feststeht
        query2 = "INSERT INTO public.private_customer (customer_id, name, geb_date) VALUES (%s, %s, %s)"
        data2 = (str(self.id), self.name, self.geb_date)

        queries.append((query2, data2))
        return queries