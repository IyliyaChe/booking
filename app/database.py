from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import NullPool

from app.config import settings
#DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

#DATABASE_PARAMS = {"poolclass": NullPool}
engine_nullpool = create_async_engine(DATABASE_URL, poolclass=NullPool)


#async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#async_session_maker_nullpool = sessionmaker(engine_nullpool, class_=AsyncSession, expire_on_commit=False)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
async_session_maker_nullpool = async_sessionmaker(engine_nullpool, expire_on_commit=False)



class Base(DeclarativeBase):
    pass