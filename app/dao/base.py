from datetime import datetime
from typing import Generic, Optional, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import and_, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import Base, async_session_maker
from app.core.logging import logger


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Класс базовых операций создания, чтения, обновления и удаления."""

    model = None

    @classmethod
    async def get_by_id(
        cls,
        obj_id: int,
    ) -> ModelType | None:
        """Возвращает объект по заданному id."""
        async with async_session_maker() as session:
            db_obj = await session.execute(
                select(cls.model).where(cls.model.id == obj_id),
            )
            return db_obj.scalars().first()

    @classmethod
    async def get_multi(cls):
        """Возврацает все объекты."""
        async with async_session_maker() as session:
            db_objs = await session.execute(select(cls.model))
            return db_objs.scalars().all()

    @classmethod
    async def create(
        cls,
        data: dict,
    ) -> ModelType:
        """Создает объект."""
        async with async_session_maker() as session:
            try:
                query = (
                    insert(cls.model).values(**data).returning(cls.model.id)
                )
                object = await session.execute(query)
                await session.commit()
                return object.mappings().first()
            except (SQLAlchemyError, Exception) as error:
                await session.rollback()
                if isinstance(error, SQLAlchemyError):
                    message = "Database Exception"
                elif isinstance(error, Exception):
                    message = "Unknown Exception"
                message += ": Не удается добавить данные."
                logger(error, message)

    @classmethod
    async def update(
        cls,
        db_obj: ModelType,
        new_data: UpdateSchemaType,
    ) -> ModelType:
        """Обновляет объект."""
        async with async_session_maker() as session:
            try:
                obj_data = jsonable_encoder(db_obj)
                for field in obj_data:
                    if field in new_data:
                        setattr(db_obj, field, new_data[field])
                session.add(db_obj)
                await session.commit()
                await session.refresh(db_obj)
                return db_obj
            except Exception as error:
                logger(error)
                session.rollback()

    @classmethod
    async def delete_object(cls, **kwargs):
        """Удаляет объект из БД."""
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**kwargs)
                result = await session.execute(query)
                result = result.scalar()
                object_to_delete = result
                if not result:
                    raise None
                await session.delete(result)
                await session.commit()
                return object_to_delete
            except:
                return None

    @classmethod
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

    @classmethod
    async def get_actual_objs(
        cls, attr_name: str, attr_value: int | str, need_actual: bool = True
    ) -> list[ModelType]:
        """
        Получить  объекты моделей БД.
        Возвращает объекты Sale_Codes или Trades.
        Опционально можно убрать фильтр актуальности,
        не будет сравниваться дата с текущим днем.
        """
        if need_actual:
            query = and_(
                getattr(cls.model, attr_name) == attr_value,
                cls.model.created_at == datetime.now().date(),
            )
        else:
            query = getattr(cls.model, attr_name) == attr_value
        async with async_session_maker() as session:
            get_objs = await session.execute(
                select(cls.model.__table__.columns).where(query)
            )
            return get_objs.mappings().all()

    @classmethod
    async def delete_old_objs(cls) -> bool:
        """Удаляет все старые записи."""
        async with async_session_maker() as session:
            try:
                await session.execute(
                    cls.model.__table__.delete().where(
                        cls.model.created_at < datetime.now().date()
                    )
                )
                await session.commit()
                return True
            except Exception as error:
                logger(error)
                return False
