
from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("email, hashed_password, status_code", [
    ("kot@pes.com", "kotopes", 200),
    ("kot@pes.com", "kot0pes", 409),
    ("pes@kot.com", "pesokot", 200),
    ("abcde", "kotopes", 422),
])
async def test_register_user(email, hashed_password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "hashed_password": hashed_password,
    })
    assert response.status_code == status_code

@pytest.mark.parametrize("email, hashed_password, status_code", [
    ("test@test.com", "test", 200),
    ("artem@example.com", "artem", 200),
])
async def test_login_user(email, hashed_password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "hashed_password": hashed_password,
    })
    assert response.status_code == status_code
