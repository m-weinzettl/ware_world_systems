
class Product:
    def __init__(self, product_id, name, price, weight):
        self.__id = product_id
        self.name = name
        self.price = price
        self.weight = weight

    @property
    def product_id(self):
        return self.__id

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self, new_price):
        self.__price = new_price

    @property
    def weight(self):
        return self.__weight
    @weight.setter
    def weight(self, new_weight):
        self.__weight = new_weight

    def __str__(self):
        return f"Product({self.name}, Preis: {self.price}€, Marke: {self.weight})"

    @staticmethod
    def get_load_query():
        return "SELECT product_id, name, price, weight FROM product"