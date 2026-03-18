#firma oder private
#gesuchte items
#generiere cart_item
import json

class Shopping_Cart:
    def __init__(self, customer, items=None):
        self.__customer = customer
        self.__items = items if items is not None else []
        self.is_company = hasattr(customer, 'uid')
        self.is_private_customer = hasattr(customer, 'geb_date')

    @property
    def customer(self):
        return self.__customer
    @property
    def items(self):
        return self.__items



    def add_item(self, product):
        self.__items.append(product)

    def get_total_price(self):
        return sum(item.price for item in self.__items)



    def generate_invoice_data(self):

        safe_name = getattr(self.__customer, "company_name", getattr(self.__customer, "name", "Unbekannt"))
        invoice = {

            "customer_info":
                {
                    "name": safe_name,
                    "address": self.__customer.address,
                    "type": "customer" if self.is_company else "private",

                },
            "items": [
                {
                    "id": str(item.product_id),
                    "name": item.name,
                    "unit_price": float(item.price),
                    "details": str(item)
                } for item in self.__items
            ],
            "total_sum": float(self.get_total_price())
        }
        return json.dumps(invoice)

    @staticmethod
    def save_invoice_query():
        return """
        INSERT INTO orders (customer_id, total_price, invoice_data, is_company_order)
        VALUES (%s, %s, %s, %s)
    """