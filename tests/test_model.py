from sqlalchemy.exc import IntegrityError
from app.models import User
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app.models import User


def test_user_model_create(db_session):
    # Begin a new transaction
    user = User(
        name="Test User",
        email="test@example.com",
        location="Test Location",
        about="Test About",
        password_hash=User.hash_password("testpassword")
    )
    db_session.add(user)
    
    # Commit the transaction
    try:
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        raise AssertionError("Failed to commit the user due to integrity error")
    
    # Ensure the user is properly saved
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.verify_password("testpassword")
    
    # Rollback the session to clean up for other tests
    db_session.rollback()

def test_user_model_create(db_session):
    user = User(
        name="Test User",
        email="test@example.com",
        location="Test Location",
        about="Test About",
        password_hash=User.hash_password("testpassword")
    )
    db_session.add(user)
    db_session.commit()
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.verify_password("testpassword")

def test_user_password_hashing():
    password = "testpassword"
    hashed = User.hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0

def test_user_password_verification():
    password = "testpassword"
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash=User.hash_password(password)
    )
    
    assert user.verify_password(password)
    assert not user.verify_password("wrongpassword")

