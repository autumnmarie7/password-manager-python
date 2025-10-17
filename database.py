import sqlite3 
# ^ python's built-in library for working with SQLite DBs
# SQLite stores data in a single file on your computer (vault.db)
import os 
# ^ gives functions for interacting with your computer's file system

def create_connection():
    os.makedirs("data", exist_ok=True)
    # ^ makes sure there's a folder called 'data'
    # if it exists, 'exist_ok=True' prevents an error
    conn = sqlite3.connect("data/vault.db") 
    # ^ connects to (or creates, if missing) a DB file called 'vault.db' inside the 'data' folder
    # ^ 'conn' variable is a connection object that lets python send SQL commands to the DB
    return conn
    # ^ gives that connection back to whatever part of your program called this function
    # 'hey, i've just created a connection to the DB - here it is. you can use it in other parts of the program'
# ^ this function opens a link to your SQLite database file

def create_tables():
    conn = create_connection() # type: ignore
    # ^ starts by calling your 'create_connection()' function to get a live DB connection
    cursor = conn.cursor()
    # ^ creates a cursor object - basically a tool that sends SQL commands to the DB

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            master_hash TEXT NOT NULL
        )
    ''')
        # ^ this runs a SQL command to create a table named 'users' if it doesn't already exist
 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            account_name TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
        # ^ creates another table named passwords, holds all your stored credentials

    conn.commit()
    # ^ saves all the changes you made to the database (like creating tables)
    conn.close()
    # ^ safely closes the connection so the DB file isn't left open
