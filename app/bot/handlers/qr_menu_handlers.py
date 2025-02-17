from random import choice
import time
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, FSInputFile, Message

from app.bot.banners import BANNERS_DIR, captions, get_file, get_img
from app.bot.constants import (
    CRITICAL_ERROR,
    DELETE_CODE,
    DELETE_ERROR,
    DWNLD_ERROR,
    FMT_GIF,
    NEXT_QR,
    NOT_FOUND,
    QR_SEND,
    SEARCH_GIFS,
    SUCCES_DNWLD,
    SUCCESS_DELETE,
)

from app.bot.handlers.callbacks.qr_menu import get_reply_for_trade, get_reply_no_trade
from app.bot.keyboards.main_menu_kb import get_btns, get_image_and_kb
from app.bot.keyboards.qr_menu_kb import get_trade_confirm_kb
from app.core.config import QR_DIR
from app.bot.filters import ImgValidationFilter, PointExistFilter, UserExistFilter
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.handlers.registration_handlers import send_ivalid_data_type_message
from app.bot.handlers.states import MenuQRStates
from app.bot.handlers.user_handlers import get_menucallback_data, process_start_command
from app.bot.keyboards.buttons import (
    ADD_QR,
    CHECK_QR,
    CONFIRM_BTNS,
    CONFIRM_SALE,
    QR_MENU,
)
from app.sale_codes.dao import Sale_CodesDAO
from app.trades.dao import TradesDAO
from app.trades.models import Trades
from app.users.dao import UsersDAO

code_router = Router()
code_router.message.filter(UserExistFilter())


@code_router.callback_query(MenuCallBack.filter(F.menu_name == DELETE_CODE))
async def process_agreed_delete(callback: CallbackQuery, callback_data: MenuCallBack):
    if await Sale_CodesDAO.delete_object(id=callback_data.code_id):
        text = SUCCESS_DELETE
    else:
        text = DELETE_ERROR
    callback_data.menu_name = QR_MENU
    await callback.answer(text=text, show_alert=True)
    await get_menucallback_data(callback, callback_data)


@code_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(
            ADD_QR,
        )
    )
)
async def process_add_code(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
):

    media, reply_markup = await get_image_and_kb(
        menu_name=callback_data.menu_name,
        user_id=callback_data.user_id,
        level=callback_data.level,
        previous_menu=QR_MENU,
    )
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await state.set_state(MenuQRStates.add_qr)


@code_router.message(
    MenuQRStates.add_qr, F.content_type == ContentType.PHOTO, ImgValidationFilter()
)
async def process_download_ok(
    message: Message,
    state: FSMContext,
    file_name: str | None,
    value: str | None,
) -> None:
    """Обработки загрузки валидного изображения."""
    user = await UsersDAO.get_by_attribute("telegram_id", message.from_user.id)
    try:
        await Sale_CodesDAO.create_code(user.id, file_name, value)
        message_text = SUCCES_DNWLD
    except:
        message_text = DWNLD_ERROR
    await message.answer(text=message_text)
    await process_start_command(message, state)
    state.clear


@code_router.message(MenuQRStates.add_qr)
async def process_download_error(
    message: Message,
    state: FSMContext,
) -> None:
    """Обработки загрузки пользователем невалидных данных."""
    await send_ivalid_data_type_message(message=message)


@code_router.callback_query(
    MenuQRStates.add_qr, MenuCallBack.filter(F.menu_name == QR_MENU)
)
async def process_qr_back_menu(
    callback: CallbackQuery,
    callback_data: CallbackQuery,
    state: FSMContext,
) -> None:
    await get_menucallback_data(callback, callback_data)
    await state.clear()


@code_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(
            CHECK_QR,
        )
    )
)
async def process_check_qr(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
) -> None:
    """
    Хэндлер для check_qr меню.
    Если в data передан trade_id - он удаляется, появляется алерт,
    если trade_id нет - идет запрос в бд, который возвращает самый первый трейд
    в текущий офис(point), либо None.
    Если трейда нет - в ответ сообщение об отсутствии их в офисе.
    Если трейд есть - редактирует собщение - меняет картинку, а в коллбэк дата
    идет уже другой trade_id.
    Таким образом при нажатии кнопки ОК будет происходить постепенный
    перебор трейдов в заданный офис, когда они закончатся - сообщение,
    что трейдов в офис нет.
    """
    # ДОБАВИТЬ ОБРАБОТКУ ОШИБКИ ОТСУТСТВИЯ КАРТИНКИ КОДА
    try:
        if callback_data.trade_id:
            await TradesDAO.delete_object(id=callback_data.trade_id)
            callback_data.trade_id = None
            trade = await TradesDAO.get_trade_by_point(callback_data.point_id)
            if trade:
                await callback.answer(text=NEXT_QR, show_alert=True)
                media, reply_markup = await get_reply_for_trade(callback_data, trade)
            else:
                media, reply_markup = await get_reply_no_trade(callback_data)
        else:
            trade = await TradesDAO.get_trade_by_point(callback_data.point_id)
            if trade:
                media, reply_markup = await get_reply_for_trade(callback_data, trade)
            else:
                media, reply_markup = await get_reply_no_trade(callback_data)
        await callback.message.edit_media(media=media, reply_markup=reply_markup)
    except:
        await callback.answer(text=CRITICAL_ERROR, show_alert=True)


@code_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(
            QR_SEND,
        )
    )
)
async def find_office(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
) -> None:
    media, reply_markup = await get_image_and_kb(
        menu_name="point_search",
        user_id=callback_data.user_id,
        level=callback_data.level,
        previous_menu=QR_MENU,
    )
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await state.set_state(MenuQRStates.point_search)


@code_router.callback_query(
    MenuQRStates.point_search,
    MenuCallBack.filter(
        F.menu_name.in_(
            "point_search",
        )
    ),
)
@code_router.message(MenuQRStates.point_search, F.content_type == ContentType.TEXT)
async def process_point_search(message: Message, state: FSMContext):
    gif = await message.answer_animation(
        animation=await get_file(filename=choice(SEARCH_GIFS), f_type=FMT_GIF),
        caption=captions.search,
    )
    if message.text.isdigit():
        if not PointExistFilter(int(message.text)):
            await message.answer_photo(photo=get_img(menu_name=NOT_FOUND))
    await gif.delete()
    # gif = await message.answer_animation(animation=)
    # if message.text.isdigit():
    #     if not PointExistFilter(message):
    #         await message.answer_photo(photo = get_img(menu_name=))


@code_router.message(MenuQRStates.point_search)
async def process_invalid_point_search_data(
    message: Message,
    state: FSMContext,
) -> None:
    """Обработки загрузки пользователем невалидных для поиска пункта."""
    await send_ivalid_data_type_message(message=message)
