import pytest
from datetime import datetime
from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id = 2,
        room_id = 2,
        date_from = datetime.strptime("2025-07-25", "%Y-%m-%d"),
        date_to = datetime.strptime("2025-07-30", "%Y-%m-%d")
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None


@pytest.mark.parametrize("user_id, room_id", [
    (1, 2),
    (1, 1),
    (2, 1), 
    (2, 2),
])
async def test_add_read_and_delete_boking(user_id, room_id):
    new_booking = await BookingDAO.add(
        user_id = user_id,
        room_id = room_id,
        date_from = datetime.strptime("2025-08-25", "%Y-%m-%d"),
        date_to = datetime.strptime("2025-08-30", "%Y-%m-%d")
        )

    assert new_booking["user_id"] == user_id
    assert new_booking["room_id"] == room_id

    get_booking = await BookingDAO.find_one_or_none(id=new_booking['id'])
    assert get_booking is not None

    await BookingDAO.delete(id=get_booking['id'])

    deleted_booking = await BookingDAO.find_one_or_none(id=new_booking["id"])
    assert deleted_booking is None