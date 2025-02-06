from fastapi import FastAPI, Query, Depends
from typing import Annotated
from datetime import date
from pydantic import BaseModel
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

app = FastAPI()

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)
app.include_router(router_rooms)


""" class SHotel(BaseModel):
    address: str
    name: str
    stars: int """

class HotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date, 
            date_to: date,
            has_spa: bool = None,
            stars: Annotated[int, Query(..., ge=1, le=5)] = None
        ):
            self.location = location
            self.date_from = date_from
            self.date_to = date_to
            self.has_spa = has_spa
            self.stars = stars


@app.get('/hotels')
def get_hotels(
        search_args: HotelsSearchArgs = Depends()
):
  return search_args