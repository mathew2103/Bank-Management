#
from init import *
from customer import *

cur, db = initialize()


def custPanel():
    cMenu = int(input("1. Create Account\n2. Login\nEnter your desired option: "))
    if cMenu == 1:
        createAcc(cur, db)
        login(cur, db)
    elif cMenu == 2:
        login(cur, db)
        pass


if cur == None:
    pass
else:
    print("-" * 20 + "Welcome to Bank Management System" + "-" * 20)
    print("1. Customer Panel\n2. Admin Panel")
    i = int(input("Enter the panel you want to visit: "))

    if i == 1:
        custPanel()
