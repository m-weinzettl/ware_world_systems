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
