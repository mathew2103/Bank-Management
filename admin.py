from tabulate import tabulate
from init import check_closed


def updatecustdetails(cur, db):
    print("-" * 20 + "UPDATE ACCOUNT" + "-" * 20)
    accno = int(input("Enter Account Number: ") or 0)
    cur.execute(f"SELECT *,IF(closed, 'Yes', 'No') FROM accounts WHERE accno={accno}")
    x = cur.fetchone()
    x = x[0:-2] + (x[-1],)
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
                "Closed",
            ],
            tablefmt="github",
        )
    )
    y = int(input("Menu- \n1. Name \n2. Security Question\nEnter:") or 0)
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

    cur.execute(f"SELECT *,IF(closed, 'Yes', 'No') FROM accounts WHERE accno={accno}")
    c = cur.fetchone()
    c = c[0:-2] + (c[-1],)
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
                "Closed",
            ],
            tablefmt="github",
        )
    )


def viewcust(cur, db):
    print("-" * 20 + "VIEW CUSTOMER DETAILS" + "-" * 20)
    cur.execute(f"SELECT accno,name,balance,IF(closed, 'Yes', 'No') FROM accounts ")
    d = cur.fetchall()
    print(
        tabulate(d, ["Account Number", "Name", "Balance", "Closed"], tablefmt="github")
    )
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


def view_all_transactions(cur, db):
    print("-" * 20 + "CHECK TRANSACTIONS" + "-" * 20)
    cur.execute(f"SELECT * from transactions order by at desc")
    b = cur.fetchall()
    print(
        tabulate(
            b, ["ID", "Sender Acc", "Receiver Acc", "At", "Amount"], tablefmt="github"
        )
    )
    return


def searchcustomer(cur, db):
    print("-" * 20 + "SEARCH CUSTOMERS" + "-" * 20)
    c = int(input("Enter account number: ") or 0)
    cur.execute(f"SELECT *,IF(closed,'Yes','No') from ACCOUNTS where accNo={c}")
    acc = cur.fetchone()
    acc = acc[0:-1] + (acc[-1],)
    if acc == None:
        print("No account found")
        return
    print(
        tabulate(
            [acc],
            [
                "Account Number",
                "Name",
                "Balance",
                "Password",
                "Security Question",
                "Security Answer",
                "Closed",
            ],
            tablefmt="github",
        )
    )


def revert_transaction(cur, db):
    print("-" * 20 + "REVERT TRANSACTION" + "-" * 20)
    i = int(input("Enter transaction id: ") or 0)
    cur.execute(f"SELECT * from transactions where id={i}")
    tr = cur.fetchone()

    if tr == None:
        print("No transaction found")
        return
    print(
        tabulate([tr], ["ID", "Sender", "Receiver", "At", "Amount"], tablefmt="github")
    )

    amt = tr[4]
    sender = tr[1]
    receiver = tr[2]

    if check_closed(sender, cur, db):
        print(f"Account number {sender} has been closed. Can't revert transaction!")
        return
    elif check_closed(receiver, cur, db):
        print(f"Account number {receiver} has been closed. Can't revert transaction!")
        return

    if input("Do you want to revert this transaction? (Yes/No)").lower() == "yes":
        cur.execute(f"UPDATE accounts SET balance=balance-{amt} where accNo={receiver}")
        cur.execute(f"UPDATE accounts SET balance=balance+{amt} where accNo={sender}")
        cur.execute(f"DELETE from transactions where id={i}")
        cur.execute(
            f"INSERT INTO notifications (accNo, content) values ({receiver}, 'Transaction reverted! -{amt}')"
        )
        cur.execute(
            f"INSERT INTO notifications (accNo, content) values ({sender}, 'Transaction reverted! +{amt}')"
        )

        print("Transaction Reverted!")


def addMoney(cur, db):
    accNo2 = int(input("Enter recipient account number: ") or 0)
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
    cur.execute(f"UPDATE accounts SET balance=balance+{m} where accNo={accNo2}")
    cur.execute(
        f"INSERT INTO notifications (accNo, content) values ({accNo2}, 'Added {m}')"
    )
    print(f"Successfully added {m} to {rec[0]}")
