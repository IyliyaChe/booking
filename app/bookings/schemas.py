from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import date


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(from_attributes=True)

class SFullBooking(SBooking):
    image_id: int
    name: str
    description: Optional[str]
    services: List[str]

    model_config = ConfigDict(from_attributes=True)

class SNewBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date

    model_config = ConfigDict(from_attributes=True)