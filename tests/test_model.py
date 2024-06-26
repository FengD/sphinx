import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..sphinx.model import User, Base
from database.create_db import generate_uuid, get_password_hash

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_user_creation(session):
    user = User(
        id=1,
        uuid=generate_uuid(),
        username="test_user",
        hashed_password=get_password_hash("password"),
        email="test@example.com",
        address="123 Test St",
        mobile=1234567890.0,
        created_at=datetime.now()
    )
    session.add(user)
    session.commit()
    queried_user = session.query(User).filter_by(username="test_user").first()
    assert queried_user is not None
    assert queried_user.username == "test_user"
    assert queried_user.email == "test@example.com"
    assert queried_user.address == "123 Test St"
    assert queried_user.mobile == 1234567890.0

def test_user_repr():
    user = User(
        uuid="test-uuid",
        username="test_user",
        hashed_password="hashed_password"
    )
    repr_str = repr(user)
    expected_str = "<User(uuid=test-uuid, username=test_user, hashed_password=hashed_password)>"
    assert repr_str == expected_str