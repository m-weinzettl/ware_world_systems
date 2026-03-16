from model.product import Product

class Electronic(Product):
    def __init__(self, name, price, weight, brand, guarantee):
        super().__init__(name, price, weight)
        self.brand = brand
        self.guarantee = guarantee

    @property
    def brand(self):
        return self.__brand

    @brand.setter
    def brand(self, new_brand):
        self.__brand = new_brand

    @property
    def guarantee(self):
        return self.__guarantee

    @guarantee.setter
    def guarantee(self, new_guarantee):
        self.__guarantee = new_guarantee

    def __str__(self):
        return f"Produkt: {self.name} | Gewicht: {self.weight} | Preis: {self.price}€ | Marke: {self.brand} | Garantie: {self.guarantee}"