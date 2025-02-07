"""Модуль главного и других меню."""

from aiogram.types import FSInputFile, InlineKeyboardMarkup, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.main_menu import get_main_menu_btns
from app.core.config import STATIC_DIR

from app.core.logging import get_logger
from app.bot.banners import Images
from app.users.models import Users

logger = get_logger(__name__)


async def main_menu(
    level: int,
    menu_name: str,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Возвращает главное меню."""
    return (
        await Images.get_img(menu_name, level),
        get_main_menu_btns(level=level),
    )


async def profile_menu(
    level: int,
    menu_name: str,
    user: Users,
    session: AsyncSession,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить состояние переключателей и вывести."""
    pass


# async def get_menu_content(
#     level: int,
#     menu_name: str,
#     user: Users,
# ) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
#     """Возвращает контент в зависимости от level и menu_name."""
#     match level:
#         case 0:
#             if menu_name == DIET:
#                 return await calorie_counter(level, menu_name, user, session)
#             if menu_name == SETTINGS:
#                 return await settings_menu(level, menu_name, user, session)
#             return await main_menu(level, menu_name)
#         case 1:
#             if menu_name == SleepMode.SLEEP:
#                 return await sleep_mode_menu(level, menu_name)
#             return await select_workout(
#                 session,
#                 level,
#                 menu_name,
#             )
#         case 2:
#             if menu_name == SleepMode.GO_TO_BED:
#                 return await go_to_bed_menu(level, menu_name, user, session)
#             if menu_name == SleepMode.WAKE_UP:
#                 return await wake_up_menu(level, menu_name, user, session)
#             if menu_name == SleepMode.DURATION:
#                 return await sleep_duration_menu(level, menu_name)
#             if menu_name == SleepMode.STATISTIC:
#                 return await sleep_statistic_menu(
#                     level,
#                     menu_name,
#                     user,
#                     session,
#                 )
