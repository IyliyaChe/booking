from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

""" class Hotels(Base):
    __tablename__ = 'hotels'
    id= Column(Integer, primary_key = True, nullable=False)
    name = Column(String, nullable = False)
    location= Column(String, nullable = False)
    services= Column(JSON)
    rooms_quantity= Column(Integer, nullable = False)
    image_id= Column(Integer) """

class Hotels(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON)
    room_quantity: Mapped[int]
    image_id: Mapped[int]

