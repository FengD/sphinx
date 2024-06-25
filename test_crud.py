import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from crud import get_user_by_id, get_user_by_username, create_user, update_user_by_id, delete_user_by_id, create_access_token, decode_access_token, authenticate_user
from database.create_db import get_password_hash, verify_password

Base = declarative_base()

DATABASE_URL = "sqlite:///./database/test_sphinx.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    user = create_user(db, "testuser", "password")
    assert user.username == "testuser"
    assert verify_password("password", user.hashed_password)

def test_get_user_by_username(db):
    user = get_user_by_username(db, "testuser")
    assert user is not None
    assert user.username == "testuser"

def test_get_user_by_id(db):
    user = get_user_by_username(db, "testuser")
    user_by_id = get_user_by_id(db, user.id)
    assert user_by_id is not None
    assert user_by_id.username == "testuser"

def test_update_user_by_id(db):
    user = get_user_by_username(db, "testuser")
    update_user_by_id(db, user.id, {"username": "updateduser"})
    updated_user = get_user_by_id(db, user.id)
    assert updated_user.username == "updateduser"

def test_delete_user_by_id(db):
    user = get_user_by_username(db, "updateduser")
    result = delete_user_by_id(db, user.id)
    assert result is True
    deleted_user = get_user_by_id(db, user.id)
    assert deleted_user is None

def test_create_access_token():
    token = create_access_token(data={"token": "testuser"})
    decoded = decode_access_token(token)
    assert decoded["token"] == "testuser"

def test_authenticate_user(db):
    create_user(db, "authuser", "authpassword")
    token = authenticate_user(db, "authuser", "authpassword")
    assert token is not False
    decoded = decode_access_token(token)
    assert decoded["token"] == "authuser"
    user = get_user_by_username(db, "authuser")
    result = delete_user_by_id(db, user.id)
