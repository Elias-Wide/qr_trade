from datetime import datetime
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from app.bot.handlers.callbacks.main_menu import (
    get_menucallback_data,
    procces_main_menu_comand,
)
from app.bot.keyboards.banners import captions, get_img
from app.bot.constants import CRITICAL_ERROR, DATE_FORMAT, NOTIFICATION_TYPE, POINT_ID, TYPE_POINT

from app.bot.keyboards.calendar_btn import get_days_btns
from app.bot.utils import get_schedule_caption
from app.core.config import QR_DIR
from app.core.logging import logger
from app.bot.filters import (
    ImgValidationFilter,
    PointExistFilter,
    UserExistFilter,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.handlers.registration_handlers import (
    send_ivalid_data_type_message,
)
from app.bot.handlers.states import ProfileStates
from app.bot.keyboards.buttons import (
    CHANGE_POINT,
    CONFIRM_SCHEDULE,
    PROFILE,
    SCHEDULE,
)
from app.bot.keyboards.main_menu_kb import get_btns
from app.points.models import Points
from app.schedules.dao import SchedulesDAO
from app.users.dao import UsersDAO


profile_router = Router()
profile_router.message.filter(UserExistFilter())


@profile_router.callback_query(
    MenuCallBack.filter(F.menu_name.in_(CHANGE_POINT))
)
async def profile_menu(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
) -> None:
    """Обработка нажатия меню профиля."""
    await state.set_state(ProfileStates.change_point)
    await callback.message.edit_caption(
        caption=TYPE_POINT,
        reply_markup=await get_btns(
            menu_name=CHANGE_POINT, level=2, previous_menu=PROFILE
        ),
    )
    await callback.answer()


@profile_router.message(
    ProfileStates.change_point, F.text.isdigit(), PointExistFilter()
)
async def change_user_point(
    message: Message, state: FSMContext, telegram_id: int, point_id: Points
) -> None:
    logger()
    user = await UsersDAO.get_by_attribute(
        attr_name="telegram_id", attr_value=telegram_id
    )
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


@profile_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(
            tuple(notice_type[0] for notice_type in NOTIFICATION_TYPE)
        )
    )
)
async def set_notice_type(
    callback: CallbackQuery, callback_data: MenuCallBack
) -> None:
    """Обработка нажатие кнопки для смены режима увеодмлений."""
    # await NotificationsDAO.set_nonification_type(user_id=callback_data.user_id, notice_type=callback_data.menu_name)
    logger(callback_data)
    await SchedulesDAO.set_nonification_type(
        callback_data.user_id, callback_data.menu_name
    )
    await callback.answer("Изменения сохранены!")
    callback_data.level, callback_data.menu_name = 1, PROFILE
    await get_menucallback_data(callback, callback_data)


@profile_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(SCHEDULE,)
    ), default_state
)
async def set_user_schedule(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
) -> None:
    """Меню графика, отдаем клавиатуру с календарем."""
    user_schedule = await SchedulesDAO.get_user_schedule(user_id=callback_data.user_id)
    logger(user_schedule)
    user_schedule = [
        datetime.strptime(date_str, DATE_FORMAT).date() for date_str in user_schedule[0]
    ]   
    await callback.message.edit_media(
        media=await get_img(SCHEDULE, caption=await get_schedule_caption()),
        reply_markup=await get_days_btns(user_id=callback_data.user_id, level=callback_data.level, user_schedule=user_schedule.copy())
    )
    await state.update_data(user_schedule=sorted(user_schedule))
    await state.set_state(ProfileStates.schedule)
    
@profile_router.callback_query(ProfileStates.schedule, MenuCallBack.filter(
        F.menu_name.in_((SCHEDULE, CONFIRM_SCHEDULE))
    )
)
async def procce_set_schedule(callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext):
    """Обработка нажатий кнопок календаря."""
    if callback_data.menu_name == CONFIRM_SCHEDULE:
        try:
            logger()
            user_schedule = (await state.get_data())["user_schedule"]
            user_schedule_list_date_str = [
                date.strftime(DATE_FORMAT) for date in user_schedule
            ]
            await SchedulesDAO.set_schedule(user_id=callback_data.user_id, date_list = user_schedule_list_date_str)
            await state.clear()
            await callback.answer(text="График успешно сохранен. Не забудьте включить уведомления по графику.")
            callback_data.level, callback_data.menu_name = 1, PROFILE
            await get_menucallback_data(callback, callback_data)
        except:
            logger("CONFIRM_SCHEDULE ERROR")
            await callback.answer(text=CRITICAL_ERROR, show_alert=True)
    else:
        user_schedule = (await state.get_data())["user_schedule"]
        date = datetime.strptime(callback_data.day, DATE_FORMAT).date()
        if date in user_schedule:
            user_schedule.remove(date)
        else:
            user_schedule.append(datetime.strptime(callback_data.day, DATE_FORMAT).date())
            user_schedule = sorted(user_schedule)
        await callback.message.edit_media(
            media=await get_img(SCHEDULE, caption=await get_schedule_caption()),
            reply_markup=await get_days_btns(user_id=callback_data.user_id, level=callback_data.level, user_schedule=user_schedule.copy())
            )
    # state_data = await state.get_data()
    # logger(state_data, callback_data)
    # await callback.answer()