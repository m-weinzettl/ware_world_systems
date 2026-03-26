from model.product.product import Product


class Book(Product):
    def __init__(self, product_id, name, price, weight, autor, page_numbers):
        super().__init__(product_id, name, price, weight)
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

    @staticmethod
    def get_load_query():
        return """
                SELECT p.product_id, p.name, p.price, p.weight, b.autor, b.page_numbers 
                FROM public.product p
                JOIN public.book_product b ON p.product_id = b.product_id
            """