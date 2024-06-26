from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from database.create_db import generate_uuid, get_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, index=True)
    username = Column(String, unique = True, index=True)
    hashed_password = Column(String)
    email = Column(String)
    address = Column(String)
    mobile = Column(Float)
    created_at = Column(DateTime)
    def __init__(self, id=None, uuid=None, username=None, hashed_password=None, email=None, address=None, mobile=None, created_at=None):
        self.id = id
        self.uuid = uuid
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
        self.address = address
        self.mobile = mobile
        self.created_at = created_at

    def __repr__(self):
        return "<User(uuid={uuid}, username={username}, hashed_password={hashed_password})>".format(
            uuid=self.uuid,
            username=self.username,
            hashed_password=self.hashed_password,
        )

if __name__ == "__main__":
    user = User(id=1, uuid=generate_uuid(), username="123", hashed_password=get_password_hash('121212'), email='', address='', mobile='', created_at='2024-06-25 08:50:50')
    print(user)
