import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator, Dict
from app.database import Base, get_db
from app.main import app
from app.models import User
from app.auth.jwt import create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db_session) -> Dict:
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123",
        "location": "Test Location",
        "about": "Test About"
    }
    
    db_user = User(
        name=user_data["name"],
        email=user_data["email"],
        location=user_data["location"],
        about=user_data["about"],
        password_hash=User.hash_password(user_data["password"])
    )
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    
    return {**user_data, "id": db_user.id}

@pytest.fixture(scope="function")
def auth_headers(test_user) -> Dict[str, str]:
    access_token = create_access_token({"sub": test_user["email"]})
    return {"Authorization": f"Bearer {access_token}"}


