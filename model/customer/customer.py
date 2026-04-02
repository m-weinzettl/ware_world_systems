import uuid
from model.validator import Validator

class Customer:
    def __init__(self, customer_id, mail, tel_number, name, address, geb_date, uid):
        self.__id = customer_id if customer_id else uuid.uuid4()
        self.mail = mail
        self.tel_number = tel_number
        self.name = name
        self.address = address
        self.geb_date = geb_date
        self.uid = uid

# Getter und Setter für Klasse Customer

    @property
    def id(self):
        return self.__id

    @property
    def mail(self):
        return self.__mail

    @mail.setter
    def mail(self, new_mail):
        is_valid, result = Validator.validate_mail(new_mail)
        if is_valid:
            self.__mail = result
        else:
            self.__mail = new_mail
            print(f"Warnung: '{new_mail}' ist keine gültige E-Mail-Adresse! (Grund: {result})")

    @property
    def tel_number(self):
        return self.__tel_number

    @tel_number.setter
    def tel_number(self, new_tel_number):
        self.__tel_number = new_tel_number

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, new_address):
        self.__address = new_address

    @property
    def geb_date(self):
        return self.__geb_date

    @geb_date.setter
    def geb_date(self, new_geb_date):
        self.__geb_date = new_geb_date

    @property
    def uid(self):
        return self.__uid

    @uid.setter
    def uid(self, new_uid):
        self.__uid = new_uid

    def __str__(self):
        return f"Customer(Name: {self.name}, E-Mail: {self.mail}, Tel: {self.tel_number}, Geb-Date: {self.geb_date})"

    # In model/customer/customer.py
    # In model/customer/customer.py
    def get_save_queries(self, password):
        query = """
            INSERT INTO public.customer (customer_id, mail, tel_number, address, password) 
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING customer_id
        """
        data = (str(self.id), self.mail, self.tel_number, self.address, password)
        return [(query, data)]

    @staticmethod
    def login_query():
        return """
            SELECT c.customer_id, c.mail, c.tel_number, c.address, 
                   p.name, p.geb_date, 
                   co.company_name, co.uid_number, c.password
            FROM public.customer c
            LEFT JOIN public.private_customer p ON c.customer_id = p.customer_id
            LEFT JOIN public.company_customer co ON c.customer_id = co.customer_id
            WHERE c.mail = %s
        """

