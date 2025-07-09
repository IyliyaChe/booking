import asyncio
from fastapi import FastAPI, Query, Depends
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

from typing import Annotated
from datetime import date
from pydantic import BaseModel
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.bookings.router import router as router_bookings
from app.users.models import Users
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from app.config import settings

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from app.database import engine
from sqladmin import Admin, ModelView
from app.admin.auth import authentication_backend

@asynccontextmanager
async def lifespan(app: FastAPI):
    # при запуске
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # при выключении


# @app.on_event("startup")
# def startup():
#      redis = aioredis.from_url(f"redis://localhost:6379", encoding="utf8", decode_responses=True)
#      FastAPICache.init(RedisBackend(redis), prefix="cache")

app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_bookings)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)


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
            
# Подключение CORS, чтобы запросы к API могли приходить из браузера 
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js 
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)



@app.get('/hotels')
def get_hotels(
        search_args: HotelsSearchArgs = Depends()
):
  return search_args



admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)