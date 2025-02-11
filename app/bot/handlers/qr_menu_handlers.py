from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message

from app.bot.banners import captions, get_img
from app.bot.constants import (
    DELETE_CODE,
    DELETE_ERROR,
    DWNLD_ERROR,
    SUCCES_DNWLD,
    SUCCESS_DELETE,
)
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
    print(callback_data)
    await callback.message.edit_media(
        media=await get_img(menu_name=callback_data.menu_name),
        reply_markup=await get_back_kb(
            menu_name=QR_MENU, user_id=callback_data.user_id, level=callback_data.level
        ),
    )
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
    print(callback_data)
    print("CHECKR QR MENU HANDLER")
    codes_to_point = await TradesDAO.get_by_attribute(
        attr_name="point_id", attr_value=callback_data.point_id
    )
    if codes_to_point:
        for code in codes_to_point:
            callback.message.answer_photo(photo=await get_img(QR_MENU))
    else:
        if callback_data.point_id == 1:
            caption = captions.no_user_point
        else:
            caption = captions.point_no_qr
        await callback.message.edit_media(
            media=await get_img(menu_name="point_no_qr", caption=caption),
            reply_markup=await get_back_kb(
                menu_name=QR_MENU, user_id=callback_data.user_id
            ),
        )


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
