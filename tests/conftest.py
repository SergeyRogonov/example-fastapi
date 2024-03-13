import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = (
    "postgresql://{username}:{password}@{hostname}:{port}/{db_name}".format(
        # username=settings.test_database_username,
        # password=settings.test_database_password,
        # hostname=settings.test_database_hostname,
        # port=settings.test_database_port,
        # db_name=settings.test_database_name,
        username=settings.database_username,
        password=settings.database_password,
        hostname=settings.database_hostname,
        port=settings.database_port,
        db_name=settings.database_name,
    )
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "bob@gmail.com", "password": "pass1234"}
    response = client.post("/users/", json=user_data)
    new_user = response.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "alex@gmail.com", "password": "1234pass"}
    response = client.post("/users/", json=user_data)
    new_user = response.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }
    return client


@pytest.fixture
def test_posts(session, test_user, test_user2):
    posts_data = [
        {
            "title": "Favorite band",
            "content": "Metallica",
            "owner_id": test_user["id"],
        },
        {
            "title": "Favorite car",
            "content": "Ferrary",
            "owner_id": test_user["id"],
        },
        {
            "title": "Favorite planet",
            "content": "Earth",
            "owner_id": test_user2["id"],
        },
    ]

    session.add_all([models.Post(**item) for item in posts_data])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
