from typing import List
from pydantic import BaseModel



class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: List[str]
    quantity: int
    image_id: int

    class Config:
        from_attribute = True

class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int

    class Config:
        from_attribute = True




