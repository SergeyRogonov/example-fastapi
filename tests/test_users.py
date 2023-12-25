import pytest
from jose import jwt

from app import schemas
from app.config import settings


@pytest.mark.parametrize(
    "email, password, result",
    [
        ("fire@gmail.com", "111qwe", 201),
        ("bwefef@gmail.com", "wef", 201),
    ],
)
def test_create_user(client, email, password, result):
    response = client.post("/users/", json={"email": email, "password": password})
    new_user = schemas.User(**response.json())
    assert response.status_code == result
    assert new_user.email == email


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("bob@gmail.com", "wrongpassword", 403),
        ("wrongemail", "pass1234", 403),
        ("wrongemail", "wrongpassword", 403),
        ("bob@gmail.com", None, 422),
        (None, "pass1234", 422),
    ],
)
def test_failed_login_user(client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
