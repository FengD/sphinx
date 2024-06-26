import pytest
import os
from database.create_db import (generate_uuid, get_password_hash, verify_password, create_connection, 
                  create_table_users, insert_data_to_users, fetch_data_from_users, close_connection)

@pytest.fixture
def db():
    db_file = 'test_sphinx.db'
    conn = create_connection(db_file)
    create_table_users(conn)
    yield conn
    close_connection(conn)
    os.remove(db_file)

def test_generate_uuid():
    uid = generate_uuid()
    assert isinstance(uid, str)
    assert len(uid) == 36

def test_get_password_hash():
    password = '123456'
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True

def test_create_table_users(db):
    assert create_table_users(db) is True

def test_insert_data_to_users(db):
    uuid = generate_uuid()
    username = 'test_user'
    hashed_password = get_password_hash('password')
    email = 'test@example.com'
    address = 'test address'
    mobile = '1234567890'
    insert_data_to_users(db, uuid, username, hashed_password, email, address, mobile)
    rows = fetch_data_from_users(db)
    assert len(rows) == 1
    assert rows[0][1] == uuid
    assert rows[0][2] == username
    assert rows[0][3] == hashed_password
    assert rows[0][4] == email
    assert rows[0][5] == address
    assert rows[0][6] == mobile

def test_fetch_data_from_users(db):
    uuid = generate_uuid()
    username = 'test_user_2'
    hashed_password = get_password_hash('password2')
    email = 'test2@example.com'
    address = 'test address 2'
    mobile = '0987654321'
    insert_data_to_users(db, uuid, username, hashed_password, email, address, mobile)
    rows = fetch_data_from_users(db)
    assert len(rows) == 1
    assert rows[0][1] == uuid
    assert rows[0][2] == username
    assert rows[0][3] == hashed_password
    assert rows[0][4] == email
    assert rows[0][5] == address
    assert rows[0][6] == mobile
