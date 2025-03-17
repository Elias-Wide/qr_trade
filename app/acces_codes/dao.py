from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.acces_codes.models import Acces_Codes
from app.dao.base import BaseDAO
from app.core.database import async_session_maker


class Acces_CodesDAO(BaseDAO):
    """Crud-операции класса кода доступа к боту."""

    model = Acces_Codes

    @classmethod
    async def check_acces(
        cls,
        acces_code: str,
    ) -> bool:
        """Проверить доступ.
        Принимает код, проверяет наличие его в бд
        и есть ли еще у него активации.
        В случае успешной проверки, урезает доступный лимит
        на единицу и возращает True.
        """
        async with async_session_maker() as session:
            code_object = await session.execute(
                select(Acces_Codes).where(
                    and_(
                        Acces_Codes.value == acces_code, Acces_Codes.limit > 0
                    )
                )
            )
            code_object = code_object.scalar_one_or_none()
            if not code_object:
                return False
            code_object.limit -= 1
            await session.commit()
            await session.refresh(code_object)
            return True
