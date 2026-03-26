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
        queries = super().get_save_queries(password)

        query2 = "INSERT INTO public.company_customer (customer_id, company_name, uid_number) VALUES (%s, %s, %s)"
        data2 = (str(self.id), self.name, self.uid)

        queries.append((query2, data2))
        return queries