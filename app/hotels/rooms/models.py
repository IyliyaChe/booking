from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


""" class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key = True, nullable=False)
    hotel_id = Column(ForeignKey('hotels.id'), nullable=False)
    name = Column(String, nullable = False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer) """

class Rooms(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int]