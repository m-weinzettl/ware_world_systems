from model.product.product import Product

class Electronic(Product):
    def __init__(self,product_id, name, price, weight, brand, guarantee):
        super().__init__(product_id,name, price, weight)
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
        return f"Elektronik: {self.name} | Marke: {self.brand} | Preis: {self.price:.2f}€ | Garantie: {self.guarantee} Monate"

    @staticmethod
    def get_load_query():
        return """
                    SELECT p.product_id, p.name, p.price, p.weight, e.brand, e.guarantee_months 
                    FROM product p
                    JOIN electronic_product e ON p.product_id = e.product_id
                """