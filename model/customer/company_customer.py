from model.customer.customer import Customer


class Company_Customer(Customer):
    def __init__(self, customer_id, mail, tel_number, name, address, uid):
        super().__init__(customer_id, mail, tel_number, name, address, None, uid)

    @staticmethod
    def get_load_query():
        return """
            SELECT c.customer_id, c.mail, c.tel_number, co.company_name, c.address, co.uid_number
            FROM customer c
            JOIN company_customer co ON c.customer_id = co.customer_id
        """