from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message

from app.bot.banners import captions, get_img
from app.bot.constants import (
    CHANGE_POINT,
    DELETE_CODE,
    DELETE_ERROR,
    DWNLD_ERROR,
    SUCCES_DNWLD,
    SUCCESS_DELETE,
)
from app.core.config import QR_DIR
from app.bot.filters import ImgValidationFilter, UserExistFilter
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.handlers.registration_handlers import send_ivalid_data_type_message
from app.bot.handlers.states import MenuQRStates
from app.bot.handlers.user_handlers import get_menucallback_data, process_start_command
from app.bot.keyboards.buttons import ADD_QR, CHECK_QR, QR_MENU
from app.bot.keyboards.main_menu_kb import get_back_kb
from app.sale_codes.dao import Sale_CodesDAO
from app.trades.dao import TradesDAO
from app.users.dao import UsersDAO

profile_router = Router()
profile_router.message.filter(UserExistFilter())


@profile_router.callback_query(MenuCallBack.filter(F.menu_name.in_(CHANGE_POINT)))
async def profile_menu(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
) -> None:
    """Обработка нажатия меню профиля."""

    if not all((callback_data.user_id, callback_data.point_id)):
        user = await UsersDAO.get_by_attribute(
            attr_name="telegram_id", attr_value=callback.message.chat.id
        )
        callback_data.user_id = user.id
        callback_data.point_id = user.point_id
    await get_menucallback_data(callback, callback_data)
    await callback.answer()

# @profile_router.callback_query(
#     MenuCallBack.filter(
#         F.menu_name.in_(
#             CHANGE_POINT,
#         )
#     )
# )
