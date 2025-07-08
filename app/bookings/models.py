from typing import TYPE_CHECKING
from sqlalchemy import JSON, Column, Computed, Date, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

if TYPE_CHECKING:
    # Убирает предупреждения отсутствия импорта и неприятные подчеркивания в 
    # PyCharm и VSCode
    from app.hotels.rooms.models import Rooms
    from app.users.models import Users

""" class Bookings(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key = True, nullable=False)
    room_id = Column(ForeignKey('rooms.id'))
    user_id = Column(ForeignKey('users.id'))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed('(date_from - date_to) * price'))
    total_days = Column(Integer, Computed('date_from - date_to')) """

class Bookings(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Computed('abs(date_to - date_from) * price'))
    total_days: Mapped[int] = mapped_column(Computed('abs(date_to - date_from)'))

    rooms: Mapped["Rooms"] = relationship(back_populates="bookings")
    user: Mapped["Users"] = relationship(back_populates="bookings")

    def __str__(self):
        return f"Booking #{self.id}"
