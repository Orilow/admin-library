import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_rent_book(client, test_user, test_book, test_reader):
    login_response = client.post(
        "/login",
        json={"email": "test@library.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/rent_book",
        json={"book_id": test_book.id, "reader_id": test_reader.id},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["book_id"] == test_book.id
    assert response.json()["reader_id"] == test_reader.id

@pytest.mark.asyncio
async def test_rent_book_no_copies(client, test_user, test_book, test_reader,db):
    login_response = client.post(
        "/login",
        json={"email": "test@library.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    test_book.copies_available = 0
    db.commit()

    response = client.post(
        "/rent_book",
        json={"book_id": test_book.id, "reader_id": test_reader.id},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Нет доступных экземпляров" in response.json()["detail"]

@pytest.mark.asyncio
async def test_return_book(client, test_user, test_book, test_reader):
    login_response = client.post(
        "/login",
        json={"email": "test@library.com", "password": "testpass"}
    )
    token = login_response.json()["access_token"]

    # Создаём займ
    client.post(
        "/rent_book",
        json={"book_id": test_book.id, "reader_id": test_reader.id},
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.post(
        "/return_book",
        json={"book_id": test_book.id, "reader_id": test_reader.id},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["return_date"] is not None