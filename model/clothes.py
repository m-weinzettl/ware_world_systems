from model.product import Product

class Clothes(Product):
    def __init__(self, name, price, weight, size, color):
        super().__init__(name, price, weight)
        self.size = size
        self.color = color

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, new_size):
        self.__size = new_size

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, new_color):
        self.__color = new_color

    def __str__(self):
        return f"Kleidung: {self.name} | Farbe: {self.color} | Größe: {self.size} | Preis: {self.price}€"