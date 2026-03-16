from model.customer import Customer


class Company_Customer(Customer):
    def __init__(self, mail, tel_number, name, address, uid):
        super().__init__(mail, tel_number, name, address, geb_date=None, uid=uid)

    def validate_uid(self):
        return bool(self.uid and len(self.uid) == 16)