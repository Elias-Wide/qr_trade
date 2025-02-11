from aiogram import F, Router
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, InputMediaPhoto, Message

from app.bot.banners import captions, get_img
from app.bot.constants import DELETE_CODE, DELETE_ERROR, SUCCESS_DELETE
from app.bot.filters import ImgValidationFilter, UserExistFilter
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.handlers.states import MenuQRStates
from app.bot.handlers.user_handlers import get_menucallback_data, process_start_command
from app.bot.keyboards.buttons import ADD_QR, QR_MENU
from app.bot.keyboards.main_menu_kb import get_back_kb
from app.sale_codes.dao import Sale_CodesDAO
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
    

@code_router.callback_query(MenuCallBack.filter(F.menu_name.in_(ADD_QR,)))
async def process_add_code(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    state: FSMContext
):
    await callback.message.edit_media(
        media=await get_img(menu_name=callback_data.menu_name),
        reply_markup = await get_back_kb(
            menu_name=callback_data.menu_name,
            user_id=callback_data.user_id,
            level=callback_data.level - 1
        )
    )
    await state.set_state(MenuQRStates.add_qr)
    
@code_router.message(MenuQRStates.add_qr, F.content_type == ContentType.PHOTO, ImgValidationFilter())
async def process_download_ok(
    message: Message,
    state: FSMContext,
    file_name: str | None,
    value: str | None,
    ) -> None:
    """Обработки загрузки валидного изображения."""
    user = UsersDAO.get_by_attribute("telagram_id", message.from_user.id)
    Sale_CodesDAO.create_code
    await message.answer(
        text="Успешная загрузка!"
    )
    await process_start_command(message, state)
    state.clear
    
    