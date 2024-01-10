#
import mysql.connector
from tabulate import tabulate
from datetime import datetime
from time import sleep


def createAcc(cur, db):
    print("-" * 20 + "ACCOUNT CREATION" + "-" * 20)
    name = input("Enter your name: ")
    password = input("Enter password: ")
    secQues = input("Enter your security question: ")
    secAns = input("Enter your security answer: ")

    if name == "" or password == "" or secQues == "" or secAns == "":
        print("Invalid Input! Try again")
        return True

    cur.execute(
        "INSERT INTO accounts (name, balance, password, secQues, secAns) values (%s, 0, %s, %s, %s);",
        (name, password, secQues, secAns),
    )
    cur.execute("SELECT accNo from accounts ORDER BY accNo DESC LIMIT 1")
    x = cur.fetchone()
    print("Account Number: ", x[0])
    print("Account created successfully, please login")
    return


def login(cur, db):
    print("-" * 20 + "LOGIN" + "-" * 20)
    acc = int(input("Enter account number: ") or 0)
    password = input("Enter password: ")
    cur.execute(
        f'Select accno, name,balance,closed from accounts where accNo={acc} and password="{password}"'
    )
    x = cur.fetchone()
    if x == None:
        print("Invalid account number or password. Try again..")
        login(cur, db)
        return

    if x[3] == 1:
        print("This account has been closed!")
        return

    cur.execute(f"Select id,content from notifications where accNo={acc} and checked=0")
    notifs = cur.fetchall() or []
    print(
        tabulate(
            [list(x[0:3])],
            ["Account Number", "Account Holder", "Balance"],
            tablefmt="github",
        )
    )

    def changePass():
        cur.execute(f"SELECT secQues, secAns from accounts where accno={acc}")
        t = cur.fetchone()
        print("Security Question:", t[0])
        secans = input("Enter your security Answer: ")
        if secans != t[1]:
            print("incorrect security password")
            return
        oldPass = input("Enter old password: ")
        newPass = input("Enter new password: ")
        if newPass == "":
            print("Invalid new password!")
            return

        if input("Re-enter new password: ") == newPass:
            cur.execute(
                f"UPDATE accounts SET password='{newPass}' where accNo={acc} and password='{oldPass}'"
            )
            print("Password has been updated, please login again!")
            login(cur, db)
        else:
            print("Re-entered password did not match!")

    def transfer():
        accNo2 = int(input("Enter recipient account number: ") or 0)

        if accNo2 == acc:
            print("You cannot send money to yourself!")
            menu()
            return

        cur.execute(f"SELECT name, closed FROM accounts where accNo={accNo2}")
        rec = cur.fetchone()
        if rec == None:
            print("Invalid account number!\n")
            return
        print("Recipient:", rec[0])

        if rec[1] == 1:
            print("This account is closed. You cannot transfer money to this account!")
            return

        m = float(input("Enter amount to transfer: "))
        if x[2] < m:
            print("Insufficient balance")
            menu()
            return

        cur.execute(f"UPDATE accounts SET balance=balance-{m} where accNo={acc}")
        cur.execute(f"UPDATE accounts SET balance=balance+{m} where accNo={accNo2}")
        cur.execute(
            f"INSERT into transactions (sender, receiver, at, amount) values ({acc}, {accNo2}, '{datetime.now()}', {m})"
        )
        cur.execute(
            f"INSERT INTO notifications (accNo, content) values ({accNo2}, 'Received {m} from {x[1]}')"
        )
        print(
            f"Successfully transferred {m} to {rec[0]}.\nCurrent Balance: {float(x[2])-m}"
        )
        menu()

    def checkTransations():
        cur.execute(
            f"SELECT * FROM transactions WHERE sender={acc} or receiver={acc} ORDER BY 3 DESC"
        )
        tr = cur.fetchall()

        l = []

        for i in tr:
            if i[1] == acc:
                l.append([i[0], i[3], i[2], f"- {i[4]}"])
            else:
                l.append([i[0], i[3], i[1], f"+ {i[4]}"])

        print(tabulate(l, ["ID", "AT", "FROM/TO", "Amount"], tablefmt="github"))

    def checkNotifs():
        print(tabulate(notifs, ["Notification ID", "Content"], tablefmt="github"))
        notifIds = [0]

        for i in notifs:
            notifIds.append(i[0])

        cur.execute(f"UPDATE notifications set checked=1 where id in {tuple(notifIds)}")

    def menu():
        i = int(
            input(
                f"\n\nMenu:\n1. Show notifications ({len(notifs)})\n2. Change Password\n3. Transfer Money\n4. Check Transactions\n(To go back to previous menu press enter)\nEnter option: "
            )
            or 0
        )

        if i == 1:
            checkNotifs()
        elif i == 2:
            changePass()
        elif i == 3:
            transfer()
        elif i == 4:
            checkTransations()
        else:
            return

        sleep(3)
        menu()

    menu()
