import os
import datetime

from dotenv import load_dotenv
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.sql import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


load_dotenv()
async_engine = create_async_engine(os.getenv('DB_URL'))
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    async def save_to_db(self):
        async with AsyncSession(async_engine) as session:
            session.add(self)
            await session.commit()

    async def delete_from_db(self):
        async with AsyncSession(async_engine) as session:
            await session.delete(self)
            await session.commit()

    @staticmethod
    def get_current_time():
        return datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=4)))

    def as_dict(self):
        return self.__dict__

    def initiate(self, *args, **kwargs):
        self.__init__(*args, **kwargs)

    @classmethod
    async def get_last_n_days(cls, n_days):
        n_days_ago = datetime.datetime.now() - datetime.timedelta(days=n_days)
        statement = select(cls).where(cls.time_at > n_days_ago).order_by(cls.time_at)
        async with AsyncSession(async_engine) as session:
            result = await session.execute(statement)

        return result.scalars()

    @classmethod
    async def get_all_records(cls):
        statement = select(cls).order_by(cls.time_at)
        async with AsyncSession(async_engine) as session:
            result = await session.execute(statement)

        return result.scalars()


class FeedDogModel(BaseModel):
    __tablename__ = "dog_feedings"
    id = Column(Integer(), primary_key=True)
    by_whom = Column(String())
    time_at = Column(DateTime(timezone=True))
    portion_size = Column(Integer())

    def __init__(self, by_whom, portion_size, time_at=None):
        self.time_at = time_at or super().get_current_time()
        self.by_whom = by_whom
        self.portion_size = int(portion_size)

    def __repr__(self):
        return f"{self.__class__}:\n" \
               f"\tby_whom: {self.by_whom}, time_at: {self.time_at}, portion_size: {self.portion_size}"

    @classmethod
    async def get_last_n_days(cls, n_days) -> list["FeedDogModel"]:
        return await super().get_last_n_days(n_days)


class WalkDogModel(BaseModel):
    __tablename__ = "dog_walks"
    id = Column(Integer(), primary_key=True)
    by_whom = Column(String())
    time_at = Column(DateTime(timezone=True))

    def __init__(self, by_whom, time_at=None):
        self.time_at = time_at or super().get_current_time()
        self.by_whom = by_whom

    def __repr__(self):
        return f"{self.__class__}:\n" \
               f"\tby_whom: {self.by_whom}, time_at: {self.time_at}"

    @classmethod
    async def get_last_n_days(cls, n_days) -> list["WalkDogModel"]:
        return await super().get_last_n_days(n_days)


async def create_db_objects():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
