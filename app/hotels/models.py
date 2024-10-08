from sqlalchemy import JSON, Column, Integer, String
from app.database import Base

class Hotels(Base):
    __tablename__ = 'hotels'
    id= Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    locaton= Column(String, nullable = False)
    services= Column(JSON)
    room_quantity= Column(Integer, nullable = False)
    image_id= Column(Integer)