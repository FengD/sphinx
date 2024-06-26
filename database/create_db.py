import sqlite3
import uuid
from passlib.context import CryptContext

def generate_uuid():
    return str(uuid.uuid4())

def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table_users(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            uuid TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            hashed_password TEXT,
            email TEXT,
            address TEXT,
            mobile TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("Table created and data inserted successfully.")
    except sqlite3.IntegrityError as e:
        print("Create Tables errors.", e)
        return False
    return True

def close_connection(conn):
    conn.close()

def insert_data_to_users(conn, uuid, username, hashed_password, email, address, mobile):
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (uuid, username, hashed_password, email, address, mobile) VALUES(?, ?, ?, ?, ?, ?)', 
                    (uuid, username, hashed_password, email, address, mobile))
    except sqlite3.IntegrityError as e:
        print("Insert data errors.", e)

def fetch_data_from_users(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    return rows
    

if __name__ == "__main__":
    conn = create_connection('sphinx.db')
    if create_table_users(conn) :
        insert_data_to_users(conn, generate_uuid(), 'Noe', get_password_hash('123456'), 'test@test.com', 'test', '1234567890')
    conn.commit()

    print(fetch_data_from_users(conn))
    conn.close()

    
