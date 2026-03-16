from model.private_customer import Private_Customer


create_test_customer_private_1 = Private_Customer(mail = "hans@test.at", tel_number="06641414253", name="Hans Wurst",
                                 address="Sauerkrautalee 12", geb_date="12.12.2012")

private_2 = Private_Customer(mail = "hans.h@test.at", tel_number="06641414253", name="Hans Wurst",
                                 address="Sauerkrautalee 12", geb_date="12.12.2012")

print(create_test_customer_private_1)
print(private_2)