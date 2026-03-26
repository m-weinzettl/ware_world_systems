import json

class Shopping_Cart:
    def __init__(self, customer, items=None):
        self.__customer = customer
        self.__items = items if items is not None else []
        self.is_company = hasattr(customer, 'uid') and customer.uid is not None
        self.is_private_customer = hasattr(customer, 'geb_date') and customer.geb_date is not None

    @property
    def customer(self):
        return self.__customer

    @property
    def items(self):
        return self.__items

    def add_item(self, product):
        self.__items.append(product)

    def get_total_price(self):
        total_price = sum(float(item.price) for item in self.__items)
        total_price_off = total_price * 0.95
        total_price_dif = total_price - total_price_off
        return float(total_price_off), float(total_price_dif)

    def generate_invoice_data(self):
        final_price, discount_sum = self.get_total_price()

        invoice = {
            "customer_info": {
                "type": "customer" if self.is_company else "private",
                "name": getattr(self.__customer, "name", None),
                "company_name": getattr(self.__customer, "company_name", None),
                "address": self.__customer.address,
                "mail": self.__customer.mail,
                "uid": getattr(self.__customer, "uid", None),
                "geb_date": str(getattr(self.__customer, "geb_date", "")) if self.is_private_customer else None
            },
            "items": [
                {
                    "id": str(item.product_id),
                    "name": item.name,
                    "unit_price": float(item.price),
                    "details": str(item).replace("€", "EUR")
                } for item in self.__items
            ],
            "total_sum": float(final_price),
            "discount_sum": float(discount_sum)
        }
        return json.dumps(invoice)

    @staticmethod
    def save_invoice_query():
        return """
        INSERT INTO public.orders (customer_id, total_price, invoice_data, is_company_order)
        VALUES (%s, %s, %s, %s) RETURNING order_id
        """

    @staticmethod
    def delete_save_order():
        return """DELETE FROM public.shopping_cart WHERE customer_id = %s"""

    @staticmethod
    def get_data_query():
        return """SELECT * FROM public.orders WHERE order_id = %s"""

    @staticmethod
    def load_cart_items():
        return "SELECT product_id FROM public.shopping_cart WHERE customer_id = %s"

    @staticmethod
    def add_item_to_cart():
        return """ INSERT INTO public.shopping_cart (customer_id, product_id)
                    VALUES (%s, %s)"""