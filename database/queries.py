## load ##

def load_all_books():
    load_all_books = """
                    SELECT p.product_id, p.name, p.price, p.weight, b.autor, b.page_numbers 
                    FROM product p
                    JOIN book_product b ON p.product_id = b.product_id
                """
    return load_all_books

def load_all_clothes():
    load_all_clothes = """
                    SELECT p.product_id, p.name, p.price, p.weight, c.size, c.color 
                    FROM product p
                    JOIN clothes_product c ON p.product_id = c.product_id
                """
    return load_all_clothes

def load_all_electronics():
    load_all_electronics = """
                    SELECT p.product_id, p.name, p.price, p.weight, e.brand, e.guarantee_months 
                    FROM product p
                    JOIN electronic_product e ON p.product_id = e.product_id
                """
    return load_all_electronics

## save ##

def save_customer():
    save_customer = "INSERT INTO customer (customer_id, mail, tel_number, address) VALUES (%s, %s, %s, %s)"
    return save_customer

def save_private_customer():
    save_private_customer = "INSERT INTO private_customer (customer_id, name, geb_date) VALUES (%s, %s, %s)"
    return save_private_customer

def save_company_customer():
    save_company_customer = "INSERT INTO company_customer (customer_id, company_name, uid_number) VALUES (%s, %s, %s)"
    return save_company_customer