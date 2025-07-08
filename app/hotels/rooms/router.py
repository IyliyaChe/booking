from datetime import date, datetime, timedelta
from typing import List

from fastapi import Query
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoom, SRoomInfo
from app.hotels.router import router


from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.database import async_session_maker
from fastapi.encoders import jsonable_encoder







@router.get('/{hotel_id}/rooms')
async def get_rooms_by_time(
    hotel_id: int,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"), 
    date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SRoomInfo]:
    rooms = await RoomDAO.find_all_rooms(hotel_id, date_from, date_to)
    return rooms

@router.get("/example/no_orm")
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(
                Rooms.__table__.columns, 
                Hotels.__table__.columns, 
                Bookings.__table__.columns
            )
            .join(Hotels, Rooms.hotel_id==Hotels.id)
            .join(Bookings, Bookings.room_id==Rooms.id)
        )
        res = await session.execute(query)
        res = res.mappings().all()
        return res


@router.get("/example/orm")
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(Rooms)
            .options(joinedload(Rooms.hotel))
            .options(selectinload(Rooms.bookings))
        )
        res = await session.execute(query)
        res = res.scalars().all()
        res = jsonable_encoder(res)
        return res