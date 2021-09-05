import sqlite3
from sqlite3 import Error
from cryptography.fernet import Fernet





def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn






def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)





def insert_into_key(master_password_h, salt):
    database = r"database.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO key(master_password_h, salt)
              VALUES(?,?) '''
    cur = conn.cursor()
    data = (master_password_h, salt)
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid





def get_key():
    database = r"database.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM key ")

    data = cur.fetchone()
    key = data[1]
    return key




def get_salt():
    database = r"database.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM key ")

    data = cur.fetchone()
    salt = data[2]
    return salt





def check_if_first_time():
    database = r"database.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM key ")
    rows = cur.fetchall()
    if len(rows) == 0:
        return True
    else:
        return False
    




def insert_account_data(website, url, username, email, password):
    database = r"database.db"
    conn = create_connection(database)
    sql = ''' INSERT INTO accounts(website, url, username, email, password)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    data = (website, url, username, email, password)
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid
 




def get_all_passwords():
    database = r"database.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts ")
    data = cur.fetchall()
    return data





def find_password(website_data):
    database = r"database.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts WHERE website='%s'" % (website_data,))
    data = cur.fetchall()
    return data





def create_database():
    database = r"database.db"

    sql_create_key_table = """ CREATE TABLE IF NOT EXISTS key (
                                        id integer PRIMARY KEY,
                                        master_password_h BLOB NOT NULL,
                                        salt BLOB NOT NULL
                                    ); """



    sql_create_accounts_table = """ CREATE TABLE IF NOT EXISTS accounts (
                                        id integer PRIMARY KEY,
                                        website BLOB,
                                        url BLOB,
                                        username BLOB,
                                        email BLOB,
                                        password BLOB
                                    ); """



    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create key table
        create_table(conn, sql_create_key_table)
        create_table(conn, sql_create_accounts_table)

    else:
        print("Error! cannot create the database connection.")

