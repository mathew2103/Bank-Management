import mysql.connector as connector

credentials = {
    "user": "root",
    "host": "localhost",
    "password": "password",
    "database": "project",
}

tables = {
    "accounts": "CREATE TABLE accounts (accNo int primary key AUTO_INCREMENT, name varchar(50), balance decimal(11,2), password varchar(50),secQues varchar(50), secAns varchar(50), closed boolean default false);",
    "transactions": "CREATE TABLE transactions (sender int, foreign key (sender) references accounts(accNo), receiver int, foreign key (receiver) references accounts(accNo), at timestamp, amount decimal(11,2));",
}

# NOTIFICATIONS


def initialize():
    try:
        db = connector.connect(
            user=credentials["user"],
            host=credentials["host"],
            password=credentials["password"],
            database=credentials["database"],
            autocommit=True,
        )
        print("Connected to Database")
    except connector.Error as err:
        print("Error:", err)
        return None

    cur = db.cursor()
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
