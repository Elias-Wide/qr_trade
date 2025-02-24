import os
from random import choice
import time
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, ContentType, FSInputFile, Message

from app.bot.handlers.callbacks.menu_processor import get_menu_content
from app.bot.keyboards.banners import BANNERS_DIR, captions, get_file, get_img
from app.bot.constants import (
    CRITICAL_ERROR,
    DELETE_CODE,
    DELETE_ERROR,
    DWNLD_ERROR,
    FMT_GIF,
    FMT_JPG,
    NEXT_QR,
    NOT_FOUND,
    SEARCH_GIFS,
    SUCCES_DNWLD,
    SUCCES_UPDATE,
    SUCCESS_DELETE,
)

from app.bot.handlers.callbacks.qr_menu import get_reply_for_trade, get_reply_no_trade
from app.bot.keyboards.main_menu_kb import get_btns, get_image_and_kb
from app.bot.keyboards.qr_menu_kb import get_point_list_kb
from app.bot.utils import delete_file, get_point_list_caption
from app.core.config import QR_DIR
from app.bot.filters import ImgValidationFilter, PointExistFilter, UserExistFilter
from app.core.logging import logger
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.handlers.registration_handlers import send_ivalid_data_type_message
from app.bot.handlers.states import MenuQRStates
from app.bot.handlers.user_handlers import get_menucallback_data, process_start_command
from app.bot.keyboards.buttons import (
    ADD_QR,
    CANCEL,
    CHECK_QR,
    CONFIRM_BTNS,
    CONFIRM_SALE,
    CONFIRM_SEND,
    CONFIRM_SEND_BTNS,
    POINT_SEARCH,
    QR_MENU,
)
from app.points.dao import PointsDAO
from app.sale_codes.dao import Sale_CodesDAO
from app.trades.dao import TradesDAO
from app.trades.models import Trades
from app.users.dao import UsersDAO

code_router = Router()
code_router.message.filter(UserExistFilter())


@code_router.callback_query(MenuCallBack.filter(F.menu_name == DELETE_CODE))
async def process_agreed_delete(callback: CallbackQuery, callback_data: MenuCallBack):
    deleted_obj = await Sale_CodesDAO.delete_object(id=callback_data.code_id)
    # await delete_file(QR_DIR, deleted_obj.file_name)
    print(deleted_obj.file_name)
    if deleted_obj:
        await delete_file(QR_DIR, deleted_obj.file_name)
        text = SUCCESS_DELETE
    else:
        text = DELETE_ERROR
    callback_data.menu_name = QR_MENU
    callback_data.level = 1
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
    answer = await Sale_CodesDAO.create_code_or_update(user.id, file_name, value)
    if answer == "create":
        message_text = SUCCES_DNWLD.format(value)
    elif answer == "update":
        message_text = SUCCES_UPDATE.format(value)
    await message.answer(text=message_text)
    await process_start_command(message, state)
    await state.clear()
    # try:
    #     print("TRY")
    #     user = await UsersDAO.get_by_attribute("telegram_id", message.from_user.id)
    #     answer = await Sale_CodesDAO.create_code_or_update(user.id, file_name, value)
    #     if answer == "create":
    #         message_text = SUCCES_DNWLD
    #     elif answer == "update":
    #         message_text = SUCCES_UPDATE
    # except:
    #     os.remove(QR_DIR / (file_name + FMT_JPG))
    #     message_text = DWNLD_ERROR
    # await message.answer(text=message_text)
    # await process_start_command(message, state)
    # state.clear


@code_router.message(MenuQRStates.add_qr)
async def process_download_error(
    message: Message,
    state: FSMContext,
) -> None:
    logger()
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
    logger()
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
        logger(callback_data)
        if callback_data.trade_id:
            await TradesDAO.delete_object(id=callback_data.trade_id)
            callback_data.trade_id = None
            user = await UsersDAO.get_by_id(callback_data.user_id)
            trade = await TradesDAO.get_trade_by_point(user.point_id)
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
            POINT_SEARCH,
        )
    ),
    default_state
)
async def find_office(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
) -> None:
    logger()
    media, reply_markup = await get_image_and_kb(
        menu_name=POINT_SEARCH,
        user_id=callback_data.user_id,
        level=callback_data.level,
        previous_menu=QR_MENU,
    )
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await state.set_state(MenuQRStates.point_search)
    await state.update_data(user_id=callback_data.user_id, code_id=callback_data.code_id, points=dict())

# @code_router.callback_query(
#     MenuQRStates.point_search,
#     MenuCallBack.filter(
#         F.menu_name.in_(
#             POINT_SEARCH,
#         )
#     ),
# )
# async def proccess_find_point(callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext):
#     message = callback.message
#     print(message)   
#     await process_point_search(message, state)

@code_router.callback_query(
    MenuQRStates.point_search,
    MenuCallBack.filter(
        F.menu_name.in_(
            POINT_SEARCH,
        )
    ),
)
async def procces_add_point(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    state: FSMContext,
):
    logger()
    state_data = await state.get_data()
    point = await PointsDAO.get_by_attribute(attr_name="point_id", attr_value=callback_data.point_id)
    state_data["points"][point.point_id] = point
    await callback.message.edit_media(
        media=await get_img(
            POINT_SEARCH,
            caption=await get_point_list_caption(state_data["points"])
        ),
        reply_markup=await get_btns(
                    menu_name=POINT_SEARCH,
                    next_menu=CONFIRM_SEND,
                    btns_data=CONFIRM_SEND_BTNS,
                    previous_menu=QR_MENU,
                    level=2
                )
    )
    await state.update_data(points=state_data["points"])

@code_router.message(MenuQRStates.point_search, F.content_type == ContentType.TEXT)
async def process_point_search(message: Message, state: FSMContext):
    # gif = await message.answer_animation(
    #     animation=await get_file(filename=choice(SEARCH_GIFS), f_type=FMT_GIF),
    #     caption=captions.search,
    # )
    print(message.text)
    logger()
    state_data = await state.get_data()
    if message.text.isdigit():
        point_filter = PointExistFilter()
        point = await point_filter(message)
        if not point:
            await message.answer_photo(
                photo=await get_file(NOT_FOUND),
                caption=captions.not_found
            )
        else:
            state_data["points"][point.point_id] = point
            logger(state_data)
            await message.answer_photo(
                photo=await get_file(POINT_SEARCH),
                caption=await get_point_list_caption(state_data["points"],),
                reply_markup=await get_btns(
                    menu_name=POINT_SEARCH,
                    next_menu=CONFIRM_SEND,
                    btns_data=CONFIRM_SEND_BTNS,
                    previous_menu=QR_MENU,
                    level=2
                )
            )
            await state.update_data(points=state_data["points"])
    else:
        if len(message.text) > 5:
            points = await PointsDAO.search_by_addres(message.text)
            if not points:
                await message.answer_photo(
                    photo=await get_file(NOT_FOUND),
                    caption=captions.not_found
                )
            else:
                await message.answer_photo(
                    photo=await get_file(POINT_SEARCH),
                    caption=captions.choose_point,
                    reply_markup=await get_point_list_kb(
                        user_id=state_data["user_id"],
                        next_menu=POINT_SEARCH,
                        points_list=points
                    )
            )
    await message.delete()


@code_router.callback_query(MenuQRStates.point_search, MenuCallBack.filter(F.menu_name.in_(CONFIRM_SEND,)))
async def process_confirm_send(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    state: FSMContext,
):
    """ОБработка подтверждения отправки кодов на пункты."""
    state_data = await state.get_data()
    logger(state_data)
    # point_data = dict()
    for point in state_data["points"].values():
        await TradesDAO.create(
            {
                "sale_code_id": state_data["code_id"],
                "user_id": state_data["user_id"],
                "point_id": point.point_id
            }
        )
    await state.clear()
    callback_data.user_id, callback_data.menu_name, callback_data.level = (
        state_data["user_id"], QR_MENU, 1
    )
    await get_menucallback_data(callback, callback_data)

@code_router.message(MenuQRStates.point_search)
async def process_invalid_point_search_data(
    message: Message,
    state: FSMContext,
) -> None:
    """Обработки загрузки пользователем невалидных для поиска пункта."""
    logger()
    await send_ivalid_data_type_message(message=message)

@code_router.callback_query(
    MenuQRStates.point_search,
     MenuCallBack.filter(
        F.menu_name.in_(
            CANCEL,
        )
    ),
)
async def procce_back_btn(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    state: FSMContext,
):
    """Отмена режима поиска пункта, переход в меню QR."""
    logger()
    callback_data.menu_name = QR_MENU
    await state.clear()
    logger(callback_data)
    await get_menucallback_data(callback, callback_data)
    
    