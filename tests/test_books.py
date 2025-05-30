import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_get_books(client):
    response = client.get("/books")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_book(client, test_user):
    login_response = client.post(
        "/login",
        json={"email": "test@library.com", "password": "testpass"}
    )
    assert login_response.status_code == status.HTTP_200_OK, f"Login failed: {login_response.json()}"
    token = login_response.json()["access_token"]

    response = client.post(
        "/books",
        json={
            "title": "New Book",
            "author": "New Author",
            "year_published": 2021,
            "isbn": "9876543210987",
            "copies_available": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(response.headers);
    assert response.status_code == status.HTTP_201_CREATED, f"Create book failed: {response.json()}"
    assert response.json()["title"] == "New Book"

@pytest.mark.asyncio
async def test_create_book_unauthorized(client):
    response = client.post(
        "/books",
        json={
            "title": "New Book",
            "author": "New Author",
            "year_published": 2021,
            "isbn": "9876543210987",
            "copies_available": 1
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED