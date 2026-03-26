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

    def get_save_queries(self, password):
        query1 = "INSERT INTO public.customer (mail, tel_number, address, password) VALUES (%s, %s, %s, %s) RETURNING customer_id"
        data1 = (self.mail, self.tel_number, self.address, password)

        query2 = "INSERT INTO public.company_customer (customer_id, company_name, uid_number) VALUES (%s, %s, %s)"
        data2 = (None, self.name, self.uid)

        return [(query1, data1), (query2, data2)]