from fastapi import FastAPI, Query
from typing import Annotated
from datetime import date

app = FastAPI(title="BookingApp",
    description="MDtext",
    summary="My first app",
    version="0.0.1",
)

@app.get('/hotels')
def get_hotels(
    location: str,
    date_from: date, 
    date_to: date,
    has_spa: bool = None,
    stars: Annotated[int, Query(..., ge=1, le=5)] = None
    ):
    return date_from, date_to
