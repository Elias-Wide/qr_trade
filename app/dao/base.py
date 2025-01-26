from sqlalchemy import insert, select

from app.core.database import async_session_maker


class BaseDAO:
    """Базовый класс CRUD операций БД."""
    model = None

    @classmethod
    async def get_by_id(cls, object_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=object_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            object = await session.execute(query)
            await session.commit()
            return object.scalars().all()
