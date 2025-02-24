from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message

from app.bot.handlers.callbacks.main_menu import procces_main_menu_comand
from app.bot.keyboards.banners import captions, get_img
from app.bot.constants import NOTIFICATION_TYPE, POINT_ID, TYPE_POINT

from app.bot.keyboards.main_menu_kb import get_btns
from app.core.config import QR_DIR
from app.bot.filters import ImgValidationFilter, PointExistFilter, UserExistFilter
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.handlers.registration_handlers import send_ivalid_data_type_message
from app.bot.handlers.states import MenuQRStates, ProfileStates
from app.bot.handlers.user_handlers import get_menucallback_data, process_start_command
from app.bot.keyboards.buttons import ADD_QR, CHANGE_POINT, CHECK_QR, PROFILE, QR_MENU
from app.core.logging import logger
from app.notifications.dao import NotificationsDAO
from app.points.models import Points
from app.sale_codes.dao import Sale_CodesDAO
from app.trades.dao import TradesDAO
from app.users.dao import UsersDAO
from app.users.models import Users
profile_router = Router()
profile_router.message.filter(UserExistFilter())


@profile_router.callback_query(MenuCallBack.filter(F.menu_name.in_(CHANGE_POINT)))
async def profile_menu(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    state: FSMContext
) -> None:
    """Обработка нажатия меню профиля."""
    await state.set_state(ProfileStates.change_point)
    await callback.message.edit_caption(caption=TYPE_POINT,
                                        reply_markup=await get_btns(
                                            menu_name=CHANGE_POINT,
                                            level=2,
                                            previous_menu=PROFILE
                                        ))
    await callback.answer()


@profile_router.message(ProfileStates.change_point, F.text.isdigit(), PointExistFilter())
async def change_user_point(message: Message, state: FSMContext,telegram_id: int, point_id: Points) -> None:
    logger()
    user = await UsersDAO.get_by_attribute(attr_name="telegram_id", attr_value=telegram_id)
    await UsersDAO.update(user, {"point_id": point_id})
    await message.delete()
    await state.clear()
    await procces_main_menu_comand(message, level=1, menu_name=PROFILE)


@profile_router.message(ProfileStates.change_point, ~F.text.isdigit())
async def handle_invalid_point_id_change(message: Message):
    """Сообщение а невалидном типе данных при смене пункта."""
    await send_ivalid_data_type_message(message)
    
@profile_router.message(
    ProfileStates.change_point, F.text.isdigit(), ~PointExistFilter()
)
async def handle_point_id_not_in_db(message: Message) -> None:
    """Сообщение о введенном невалидном point id."""
    await send_ivalid_data_type_message(data_type=POINT_ID, message=message)


@profile_router.callback_query(MenuCallBack.filter(
    F.menu_name.in_(tuple(notice_type[0] for notice_type in NOTIFICATION_TYPE))
))
async def set_notice_type(callback: CallbackQuery, callback_data: MenuCallBack) -> None:
    # await NotificationsDAO.set_nonification_type(user_id=callback_data.user_id, notice_type=callback_data.menu_name)
    logger(callback_data)
    
    
