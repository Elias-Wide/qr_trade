from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """Родительский класс для базового."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Возвращает имя для таблицы в нижнем регистре."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


engine = create_async_engine(settings.DB_URL)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase, PreBase):
    pass
