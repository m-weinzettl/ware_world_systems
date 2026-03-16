from model.customer import Customer

class Private_Customer(Customer):
    def __init__(self, mail, tel_number, name, address, geb_date):
        super().__init__(mail, tel_number, name, address, geb_date=geb_date, uid=None)

    def calculate_age(self):
        print(f"Berechne Alter für {self.name}")