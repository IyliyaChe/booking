from datetime import date

from pydantic import parse_obj_as
from pydantic import TypeAdapter
from app.exceptions import RoomCannotBeBooked, BookingNotExist
from app.users.dao import UserDAO
from app.users.dependences import get_current_user, get_token
from app.users.models import Users
from fastapi import APIRouter, Request, Depends
from sqlalchemy import select
from app.bookings.dao import BookingDAO
from app.tasks.tasks import send_booking_confirmation_email
from fastapi import BackgroundTasks


from app.bookings.schemas import SBooking, SFullBooking, SNewBooking
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
#    room_id: int,
#    date_from: date,
#    date_to: date,
    background_tasks:BackgroundTasks,
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, booking.room_id, booking.date_from, booking.date_to)
    if not booking:
        raise RoomCannotBeBooked
 #  booking_dict = parse_obj_as(SBooking, booking).dict()
    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()

    #вариант с celery
    send_booking_confirmation_email.delay(booking, user.email)
    
    #вариант с background_tasks
    #background_tasks.add_task(send_booking_confirmation_email, booking, user.email)
    return booking

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


