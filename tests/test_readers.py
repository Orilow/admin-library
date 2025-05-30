import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_get_readers(client, test_user):
    login_response = client.post(
        "/login",
        json={"email": "test@library.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    response = client.get("/readers", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_reader(client, test_user):
    login_response = client.post(
        "/login",
        json={"email": "test@library.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/readers",
        json={"name": "New Reader", "email": "newreader@library.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["email"] == "newreader@library.com"