from model.product import Product

class book(Product):
    def __init__(self, name, price, weight, autor, page_numbers):
        super().__init__(name, price, weight)
        self.autor = autor
        self.page_numbers = page_numbers

    @property
    def autor(self):
        return self.__autor

    @autor.setter
    def autor(self, new_autor):
        self.__autor = new_autor

    @property
    def page_numbers(self):
        return self.__page_numbers

    @page_numbers.setter
    def page_numbers(self, new_page_numbers):
        self.__page_numbers = new_page_numbers

    def __str__(self):
        return f"Buchtitel: {self.name} | Autor: {self.autor} | Preis: {self.price}€"