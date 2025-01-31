from datetime import date
from app.exceptions import RoomCannotBeBooked
from app.users.dao import UserDAO
from app.users.dependences import get_current_user, get_token
from app.users.models import Users
from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from app.bookings.dao import BookingDAO


from app.bookings.schemas import SBooking
from app.database import async_session_maker
from app.bookings.models import Bookings

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования'],
)

@router.get('')
#async def get_bookings(token = Depends(get_token)): # -> list[SBooking]:
    #return await BookingDAO.find_all(user_id=1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

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


