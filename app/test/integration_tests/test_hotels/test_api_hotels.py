import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("location,date_from,date_to,status_code", [
    ("Алтай", "2030-05-31", "2030-05-15", 400),
    ("Алтай", "2030-04-15", "2030-05-31", 400),
    ("Алтай", "2026-05-15", "2026-05-31", 200),
])
async def test_get_hotels(
    location, date_from, date_to, status_code, ac: AsyncClient
):
    response = await ac.get("/hotels/{location}", params={
        "location": location,
        "date_from": date_from,
        "date_to": date_to,
    })
    print(response.status_code)
    assert response.status_code == status_code