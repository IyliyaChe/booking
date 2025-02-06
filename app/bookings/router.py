from datetime import date
from app.exceptions import RoomCannotBeBooked, BookingNotExist
from app.users.dao import UserDAO
from app.users.dependences import get_current_user, get_token
from app.users.models import Users
from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from app.bookings.dao import BookingDAO


from app.bookings.schemas import SBooking, SFullBooking
from app.database import async_session_maker
from app.bookings.models import Bookings

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования'],
)

@router.get('')
#async def get_bookings(token = Depends(get_token)): # -> list[SBooking]:
    #return await BookingDAO.find_all(user_id=1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SFullBooking]:
    return await BookingDAO.find_all_bookings(user_id=user.id)

@router.post('')
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked

@router.delete('/{booking_id}')
async def del_booking(
    booking_id: int,
    user: UserDAO = Depends(get_current_user)
):
    if not await BookingDAO.find_by_id(booking_id):
        raise BookingNotExist
    else:
        delete_booking = await BookingDAO.delete(id=booking_id, user_id = user.id)
    if not await BookingDAO.find_by_id(booking_id):
        return f"Бронирование %{booking_id} удалено"


