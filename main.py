from init import *
from customer import *
from admin import *
from time import sleep

cur, db = initialize()


def custPanel():
    print("-" * 20 + "CUSTOMER PANEL" + "-" * 20)
    cMenu = int(
        input(
            "1. Create Account\n2. Login\n(To go back to previous menu press enter)\nEnter your desired option: "
        )
        or 0
    )
    if cMenu == 1:
        x = createAcc(cur, db)
        if x == None:
            login(cur, db)
    elif cMenu == 2:
        login(cur, db)
    mainMenu()


def adminPanel():
    print("-" * 20 + "ADMIN PANEL" + "-" * 20)
    aMenu = int(
        input(
            "1. Update account details\n2. View All Customers\n3. Close Account\n4. View all transactions\n5. Search Customer by Account Number\n(To go back to previous menu press enter)\nEnter option: "
        )
        or 0
    )
    if aMenu == 1:
        updatecustdetails(cur, db)
    elif aMenu == 2:
        viewcust(cur, db)
    elif aMenu == 3:
        closeaccount(cur, db)
    elif aMenu == 4:
        checktransations(cur, db)
    elif aMenu == 5:
        searchcustomer(cur, db)
    else:
        return
    sleep(3)
    adminPanel()
    return


def mainMenu():
    print("-" * 20 + "Welcome to Bank Management System" + "-" * 20)
    print("1. Customer Panel\n2. Admin Panel")
    i = int(input("Enter the panel you want to visit: ") or 0)

    if i == 1:
        custPanel()
    elif i == 2:
        adminPanel()
    else:
        print("Invalid Input!\n")
    mainMenu()


if cur == None:
    pass
else:
    mainMenu()
