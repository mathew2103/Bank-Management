from tabulate import tabulate


def updatecustdetails(cur, db):
    print("-" * 20 + "UPDATE ACCOUNT" + "-" * 20)
    accno = int(input("Enter Account Number: "))
    cur.execute(f"SELECT * FROM accounts WHERE accno={accno}")
    x = cur.fetchone()
    print(
        tabulate(
            [list(x)],
            [
                "Account Number",
                "Name",
                "Balance",
                "Password",
                "Security Question",
                "Security Answer",
            ],
        )
    )
    y = int(input("Menu- \n1. Name \n2. Security Question\nEnter:"))
    if y == 1:
        z = input("Enter New Name: ")
        cur.execute(f"UPDATE accounts SET name='{z}' WHERE accno={accno}")
    elif y == 2:
        a = input("Enter New Security Question: ")
        b = input("Enter New Security Answer: ")
        cur.execute(
            f"UPDATE accounts SET secQues='{a}', secAns='{b}' WHERE accno={accno}"
        )
        print("Your security Question and Answer has been changed")
    cur.execute(f"SELECT * FROM accounts WHERE accno={accno}")
    c = cur.fetchone()
    print(
        tabulate(
            [c],
            [
                "Account Number",
                "Name",
                "Balance",
                "Password",
                "Security Question",
                "Security Answer",
            ],
        )
    )


def viewcust(cur, db):
    print("-" * 20 + "VIEW CUSTOMER DETAILS" + "-" * 20)
    cur.execute(f"SELECT accno,name,balance,IF(closed, 'Yes', 'No') FROM accounts ")
    d = cur.fetchall()
    print(tabulate(d, ["Account Number", "Name", "Balance", "Closed"]))
    return


def closeaccount(cur, db):
    print("-" * 20 + "CLOSE ACCOUNT" + "-" * 20)
    X = int(input("Enter Account Number: "))
    cur.execute(f"select * from Accounts where accNo={X}")
    y = cur.fetchone()

    print("Account Holder:", y[1])
    z = input("Do you want to close this account? (Yes/No) ")
    if z.lower() == "yes":
        cur.execute(f"UPDATE accounts SET closed=1 where accNo={X}")
        print("Account has been closed")
    return


def checktransations(cur, db):
    print("-" * 20 + "CHECK TRANSACTIONS" + "-" * 20)
    cur.execute(f"SELECT * from transactions order by at desc")
    b = cur.fetchall()
    print(tabulate(b, ["Sender Acc", "Receiver Acc", "At", "Amount"]))
    return


def searchcustomer(cur, db):
    print("-" * 20 + "SEARCH CUSTOMERS" + "-" * 20)
    c = int(input("enter account number"))
    cur.execute(f"SELECT * from ACCOUNTS where accNo={c}")
    k = cur.fetchone()
    print(
        tabulate(
            [k],
            [
                "Account Number",
                "Name",
                "Balance",
                "Password",
                "Security Question",
                "Security Answer",
            ],
        )
    )
