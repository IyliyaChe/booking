from datetime import date, datetime, timedelta
from typing import List
from fastapi import APIRouter, Query

from app.exceptions import CannotBookHotelForLongPeriod, DateFromCannotBeAfterDateTo
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelInfo


router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

@router.get('/{location}')
async def get_hotels(location: str, 
               date_from: date = Query(..., description=f"Например, {datetime.now().date()}"), 
               date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")
        ) -> List[SHotelInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod 
    hotels = await HotelDAO.find_all_free(location, date_from, date_to)
    return hotels