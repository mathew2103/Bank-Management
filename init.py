import mysql.connector as connector


dbName = "project"
credentials = {
    "user": "root",
    "host": "localhost",
    "password": "password",
}

tables = {
    "accounts": "CREATE TABLE accounts (accNo int primary key AUTO_INCREMENT, name varchar(50), balance decimal(11,2), password varchar(50),secQues varchar(50), secAns varchar(50), closed boolean default false);",
    "transactions": "CREATE TABLE transactions (id int AUTO_INCREMENT PRIMARY KEY, sender int, foreign key (sender) references accounts(accNo), receiver int, foreign key (receiver) references accounts(accNo), at timestamp, amount decimal(11,2));",
    "notifications": "CREATE TABLE notifications (id int AUTO_INCREMENT primary key, accNo int, foreign key (accNo) references accounts(accNo), content varchar(50), checked boolean default 0)",
}


def initialize():
    try:
        db = connector.connect(
            user=credentials["user"],
            host=credentials["host"],
            password=credentials["password"],
            autocommit=True,
        )
        print("Connected to SQL Successfully")
    except connector.Error as err:
        print("Error:", err)
        return (None, None)

    cur = db.cursor()

    cur.execute("SHOW DATABASES;")
    db_data = cur.fetchall()
    for d in db_data:
        if d[0] == dbName:
            break
    else:
        cur.execute("CREATE DATABASE project")
        print("Created project database")
    cur.execute("USE project;")
    print("Connected to database!")

    cur.execute("SHOW TABLES;")
    tables_data = cur.fetchall()
    tables_list = []
    for i in tables_data:
        tables_list.append(i[0])
    for i in tables:
        if i not in tables_list:
            cur.execute(tables[i])
            print(f"Created {i} table")

    return cur, db


def check_closed(accNo, cur, db):
    cur.execute(f"SELECT closed from accounts where accNo={accNo}")
    closed = cur.fetchone()
    return closed[0]
