from email_validator import validate_email

from model.validator import Validator
from model.customer import Customer
from model.Private_Customer import Private


create_test_customer_private_1 = Private(mail = "hans@test.at", tel_number="06641414253", name="Hans Wurst",
                                 address="Sauerkrautalee 12", geb_date="12.12.2012")

private_2 = Private(mail = "hans..@test.at", tel_number="06641414253", name="Hans Wurst",
                                 address="Sauerkrautalee 12", geb_date="12.12.2012")



print(create_test_customer_private_1.name)
print(create_test_customer_private_1.geb_date)
print(private_2.mail)
print(create_test_customer_private_1)