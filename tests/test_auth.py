import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_register(client):
    response = client.post(
        "/register",
        json={"email": "newuser@library.com", "password": "newpass123"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "newuser@library.com"

@pytest.mark.asyncio
async def test_register_existing_email(client, test_user):
    response = client.post(
        "/register",
        json={"email": "test@library.com", "password": "newpass123"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email уже занят" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login(client, test_user):
    response = client.post(
        "/login",
        json={"email": "test@library.com", "password": "testpass"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_credentials(client, test_user):
    response = client.post(
        "/login",
        json={"email": "test@library.com", "password": "wrongpass"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Неверный email или пароль" in response.json()["detail"]