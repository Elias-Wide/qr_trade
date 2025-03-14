from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, ContentType, Message

from app.bot.keyboards.banners import captions, get_file, get_img
from app.core.constants import (
    CRITICAL_ERROR,
    DELETE_CODE,
    DELETE_ERROR,
    NEXT_QR,
    NOT_FOUND,
    SUCCES_DNWLD,
    SUCCES_UPDATE,
    SUCCESS_DELETE,
    SUCCESS_SENDING,
)

from app.bot.handlers.callbacks.qr_menu import (
    get_reply_for_trade,
    get_reply_no_trade,
)
from app.bot.keyboards.main_kb_builder import get_btns, get_image_and_kb
from app.bot.keyboards.qr_menu_kb import get_point_list_kb
from app.bot.utils import delete_file, get_point_list_caption
from app.bot.filters import (
    ImgValidationFilter,
    PointExistFilter,
)
from app.core.logging import logger
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.handlers.registration_handlers import (
    send_ivalid_data_type_message,
)
from app.bot.handlers.states import MenuQRStates
from app.bot.handlers.user_handlers import (
    get_menucallback_data,
    process_start_command,
)
from app.bot.keyboards.buttons import (
    ADD_QR,
    CANCEL,
    CHECK_QR,
    CONFIRM_SEND,
    CONFIRM_SEND_BTNS,
    MAX_POINTS_LIST_MSG,
    POINT_SEARCH,
    QR_MENU,
)
from app.points.dao import PointsDAO
from app.sale_codes.dao import Sale_CodesDAO
from app.trades.dao import TradesDAO
from app.trades.models import Trades
from app.users.dao import UsersDAO

code_router = Router()


@code_router.callback_query(MenuCallBack.filter(F.menu_name == DELETE_CODE))
async def process_agreed_delete(
    callback: CallbackQuery, callback_data: MenuCallBack
):
    """Обработка нажатий кнопок удаления Sale_Codes."""
    deleted_obj = await Sale_CodesDAO.delete_object(id=callback_data.code_id)
    if deleted_obj:
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
    """Обработка нажатия кнопки НАЗАД в процессе загрузки кода."""
    media, reply_markup = await get_image_and_kb(
        menu_name=callback_data.menu_name,
        user_id=callback_data.user_id,
        level=callback_data.level,
        previous_menu=QR_MENU,
    )
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await state.set_state(MenuQRStates.add_qr)


@code_router.message(
    MenuQRStates.add_qr,
    F.content_type == ContentType.PHOTO,
    ImgValidationFilter(),
)
async def process_download_ok(
    message: Message,
    state: FSMContext,
    client_id: str | None,
    encode_value: str | None,
) -> None:
    """Обработки загрузки валидного изображения."""
    user = await UsersDAO.get_by_attribute(
        "telegram_id", message.from_user.id
    )
    answer = await Sale_CodesDAO.create_code_or_update(
        user.id, client_id, encode_value
    )
    if answer == "create":
        message_text = SUCCES_DNWLD.format(client_id)
    elif answer == "update":
        message_text = SUCCES_UPDATE.format(client_id)
    await message.answer(text=message_text)
    await process_start_command(message, state)
    await state.clear()


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
    Если в callback_data передан trade_id - он удаляется, появляется алерт,
    если trade_id нет - запрос в бд, который возвращает самый первый трейд
    в текущий офис(point), либо None.
    Если трейда нет - в ответ сообщение об отсутствии заказов на пункт.
    Если трейд есть - редактирует собщение - меняет картинку, а в коллбэк дата
    идет уже другой trade_id.
    Таким образом при нажатии кнопки ОК будет происходить постепенный
    перебор трейдов в заданный офис, когда они закончатся - сообщение,
    что заказов на пункт пользователя нет.
    """
    user = await UsersDAO.get_by_id(callback_data.user_id)
    callback_data.level = 2
    try:
        logger(callback_data)
        if callback_data.trade_id:
            await TradesDAO.delete_object(id=callback_data.trade_id)
            callback_data.trade_id = None
            trade = await TradesDAO.get_trade_by_point(user.point_id)
            if trade:
                await callback.answer(text=NEXT_QR, show_alert=True)
                media, reply_markup = await get_reply_for_trade(
                    callback_data, trade
                )
            else:
                media, reply_markup = await get_reply_no_trade(callback_data)
        else:
            trade = await TradesDAO.get_trade_by_point(user.point_id)
            logger(trade)
            if trade:
                media, reply_markup = await get_reply_for_trade(
                    callback_data, trade
                )
            else:
                media, reply_markup = await get_reply_no_trade(callback_data)
        await callback.message.edit_media(
            media=media, reply_markup=reply_markup
        )
        logger(media.caption)
        if media.caption == captions.confirm_trade:
            await delete_file(media.media.path)
    except Exception as error:
        logger(error)
        await callback.answer(text=CRITICAL_ERROR, show_alert=True)


@code_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(
            POINT_SEARCH,
        )
    ),
    default_state,
)
async def process_find_office(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
) -> None:
    """обраотка нажатия кнопки выбора кода, открытие меню поиска пункта."""
    logger()
    media, reply_markup = await get_image_and_kb(
        menu_name=POINT_SEARCH,
        user_id=callback_data.user_id,
        level=callback_data.level,
        previous_menu=QR_MENU,
    )
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await state.set_state(MenuQRStates.point_search)
    await state.update_data(
        user_id=callback_data.user_id,
        code_id=callback_data.code_id,
        points=dict(),
    )


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
    """ОБработка найденного пункта, доавление в state_data."""
    logger()
    state_data = await state.get_data()
    point = await PointsDAO.get_by_attribute(
        attr_name="point_id", attr_value=callback_data.point_id
    )
    state_data["points"][point.point_id] = point
    await callback.message.edit_media(
        media=await get_img(
            POINT_SEARCH,
            caption=await get_point_list_caption(state_data["points"]),
        ),
        reply_markup=await get_btns(
            menu_name=POINT_SEARCH,
            next_menu=CONFIRM_SEND,
            btns_data=CONFIRM_SEND_BTNS,
            previous_menu=QR_MENU,
            level=2,
        ),
    )
    await state.update_data(points=state_data["points"])


@code_router.message(
    MenuQRStates.point_search, F.content_type == ContentType.TEXT
)
async def process_point_search(message: Message, state: FSMContext):
    """
    Поиск пункта по адресу или id.
    В сообщение передается возможный адрес пункта или его id,
    осуществляется запрос в бд по выбранному параметру.
    Валидация пункта через фильтр непосредственно в хэндлере.
    """
    state_data = await state.get_data()
    logger(state_data)
    if len(state_data["points"]) > 3:
        await message.answer_photo(
            photo=await get_file(POINT_SEARCH),
            caption=MAX_POINTS_LIST_MSG
            + (
                await get_point_list_caption(
                    state_data["points"],
                )
            ),
            reply_markup=await get_btns(
                menu_name=POINT_SEARCH,
                next_menu=CONFIRM_SEND,
                btns_data=CONFIRM_SEND_BTNS,
                previous_menu=QR_MENU,
                level=2,
            ),
        )
    else:
        if message.text.isdigit():
            point_filter = PointExistFilter()
            point = (await point_filter(message))["model_obj"]
            if not point:
                await message.answer_photo(
                    photo=await get_file(NOT_FOUND),
                    caption=captions.not_found,
                )
            else:
                state_data["points"][point.point_id] = point
                await message.answer_photo(
                    photo=await get_file(POINT_SEARCH),
                    caption=await get_point_list_caption(
                        state_data["points"],
                    ),
                    reply_markup=await get_btns(
                        menu_name=POINT_SEARCH,
                        next_menu=CONFIRM_SEND,
                        btns_data=CONFIRM_SEND_BTNS,
                        previous_menu=QR_MENU,
                        level=2,
                    ),
                )
                await state.update_data(points=state_data["points"])
        else:
            if len(message.text) >= 5:
                points = await PointsDAO.search_by_addres(message.text)
                if not points:
                    await message.answer_photo(
                        photo=await get_file(NOT_FOUND),
                        caption=captions.not_found,
                    )
                else:
                    logger(len(state_data["points"]))
                    await message.answer_photo(
                        photo=await get_file(POINT_SEARCH),
                        caption=captions.choose_point,
                        reply_markup=await get_point_list_kb(
                            user_id=state_data["user_id"],
                            next_menu=POINT_SEARCH,
                            points_list=points,
                            points_in_state=state_data["points"],
                        ),
                    )
    await message.delete()


@code_router.callback_query(
    MenuQRStates.point_search,
    MenuCallBack.filter(
        F.menu_name.in_(
            CONFIRM_SEND,
        )
    ),
)
async def process_confirm_send(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    state: FSMContext,
):
    """ОБработка подтверждения отправки кодов на пункты."""
    state_data = await state.get_data()
    logger(state_data)
    for point in state_data["points"].values():
        await TradesDAO.create(
            {
                "sale_code_id": state_data["code_id"],
                "user_id": state_data["user_id"],
                "point_id": point.point_id,
            }
        )
    await state.clear()
    callback_data.user_id, callback_data.menu_name, callback_data.level = (
        state_data["user_id"],
        QR_MENU,
        1,
    )
    await callback.answer(text=SUCCESS_SENDING)
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
    await get_menucallback_data(callback, callback_data)
