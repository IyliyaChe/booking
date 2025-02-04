from datetime import date

from sqlalchemy import and_, func, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms

from app.database import async_session_maker


class RoomDAO(BaseDAO):

    model = Rooms

    @classmethod
    async def find_all_rooms(cls, hotel_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
        SELECT room_id, COUNT(room_id) AS rooms_booked
        FROM bookings
        WHERE
        (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
        (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        GROUP BY room_id
        )"""
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from, 
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from, 
                    )
                )
            )
            .group_by(Bookings.room_id)
        ).cte("booked_rooms")
        """
        SELECT *, 15*price AS total_cost, 
        (rooms.quantity - COALESCE(rooms_booked, 0)) AS rooms_left FROM rooms
        LEFT JOIN booked_rooms 
        ON rooms.id = booked_rooms.room_id
        WHERE hotel_id = 1"""
        find_hotel_rooms = (
            select(
                Rooms.__table__.columns,
                ((date_from - date_to).days * Rooms.price).label('total_cost'),
                (Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label('rooms_left')
            ).select_from(Rooms).join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
            .where(Rooms.hotel_id == hotel_id)
        )

        async with async_session_maker() as session:
            free_rooms = await session.execute(find_hotel_rooms)
            return free_rooms.mappings().all()


