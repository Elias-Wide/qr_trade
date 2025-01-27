from typing import TypeVar
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import insert, select

from app.core.database import Base, async_session_maker

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO:
    """Базовый класс CRUD операций БД."""

    model = None

    @classmethod
    async def get(
        cls,
        obj_id: int,
    ):
        """Возвращает объект по заданному id."""
        async with async_session_maker() as session:
            db_obj = await session.execute(
                select(cls.model).where(cls.model.id == obj_id),
            )
        return db_obj.scalars().first()

    async def get_multi(cls):
        """Возврацает все объекты."""
        async with async_session_maker() as session:
            db_objs = await session.execute(select(cls.model))
            return db_objs.scalars().all()

    @classmethod
    async def create(cls, obj: ModelType) -> ModelType:
        """Создает объект."""
        async with async_session_maker() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @classmethod
    async def update(
        cls,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        """Обновляет объект."""
        async with async_session_maker() as session:
            obj_data = jsonable_encoder(db_obj)
            update_data = obj_in.model_dump(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    @classmethod
    async def remove(cls, db_obj: ModelType) -> ModelType:
        """Удаляет объект."""
        async with async_session_maker() as session:
            await session.delete(db_obj)
            await session.commit()
            return db_obj

    async def get_by_attribute(
        cls,
        attr_name: str,
        attr_value: str,
    ) -> ModelType | None:
        """Возвращает объект по заданому атрибуту."""
        async with async_session_maker() as session:
            db_obj = await session.execute(
                select(cls.model).where(
                    getattr(cls.model, attr_name) == attr_value,
                ),
            )
            return db_obj.scalars().first()
