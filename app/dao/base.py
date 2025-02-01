from typing import Generic, Optional, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import logger
from app.core.database import Base, async_session_maker

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Класс базовых операций создания, чтения, обновления и удаления."""
    model = None


    @classmethod
    async def get(
        cls,
        obj_id: int,
        session: AsyncSession,
    ) -> ModelType | None:
        """Возвращает объект по заданному id."""
        db_obj = await session.execute(
            select(cls.model).where(cls.model.id == obj_id),
        )
        return db_obj.scalars().first()

    @classmethod
    async def get_multi(cls, session: AsyncSession):
        """Возврацает все объекты."""
        db_objs = await session.execute(select(cls.model))
        return db_objs.scalars().all()

    @classmethod
    async def create(
        cls,
        data: dict[Optional[int, str, bool]],
        session: AsyncSession,
    ) -> ModelType:
        """Создает объект."""
        try:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknown Exception'
            message += ': Не удается добавить данные.'

            logger.error(
                message,
                extra={'table': cls.model.__tablename__},
                exc_info=True
            )
            return None

    @classmethod
    async def update(
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """Обновляет объект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @staticmethod
    async def remove(
        db_obj: ModelType,
        session: AsyncSession,
    ) -> ModelType:
        """Удаляет объект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ) -> ModelType | None:
        """Возвращает объект по заданому атрибуту."""
        db_obj = await session.execute(
            select(self.model).where(
                getattr(self.model, attr_name) == attr_value,
            ),
        )
        return db_obj.scalars().first()