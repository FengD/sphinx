from sqlalchemy.orm import Session
from model import  User
from datetime import datetime, timedelta
from jose import JWTError, jwt
from database.create_db import get_password_hash, verify_password
from database.create_db import generate_uuid

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db : Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(uuid=generate_uuid(), username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_by_id(db: Session, user_id: int, user: User):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        return None
    for key, value in user.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_id(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        return False
    db.delete(db_user)
    db.commit()
    return True

ALGORITHM = "HS256"
SECRET_KEY = "your_secret_key"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    created_token = create_access_token(data={"token": username})
    return created_token

if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    DATABASE_URL = "sqlite:///./database/sphinx.db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with SessionLocal() as db:
        token = authenticate_user(db, 'Noe', '123456')
        print("Success: ", token)
        token = authenticate_user(db, 'Noe', '12345678')
        print("Failed: ", token)