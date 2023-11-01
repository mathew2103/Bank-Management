#
import mysql.connector
import tabulate


def createAcc(cur, db):
    print("-" * 20 + "ACCOUNT CREATION" + "-" * 20)
    name = input("Enter your name: ")
    password = input("Enter password: ")
    secQues = input("Enter your security question: ")
    secAns = input("Enter your security answer: ")
    cur.execute(
        "INSERT INTO accounts (name, balance, password, secQues, secAns) values (%s, 0, %s, %s, %s);",
        (name, password, secQues, secAns),
    )
    cur.execute("SELECT accNo from accounts ORDER BY accNo LIMIT 1")
    x = cur.fetchone()
    print(x)
    print("Account Number: ", x[0])
    print("Account created successfully, please login")
    return


def login(cur, db):
    print("-" * 20 + "LOGIN" + "-" * 20)
    accno = int(input("Enter account number: "))
    password = input("Enter password: ")
    cur.execute(
        f'Select accno, name,balance from accounts where accno={accno} and password="{password}"'
    )
    x = cur.fetchone()
    if x == None:
        print("Invalid account number or password. Try again..")
        login()
        return
    print(x)
    print(
        tabulate.tabulate(
            [list(x)], ["Account Number", "Account Holder", "Balance"], numalign="left"
        )
    )
