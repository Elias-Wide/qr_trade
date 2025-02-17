from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import (
    DEFAULT_KEYBOARD_SIZE,
    MAIN_MENU,
    NO_CAPTION,
    QR_SEND,
    QR_UPDATE,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import (
    CHECK_QR,
    DELETE_QR,
    DELETE_QR_BTN,
    QR_MENU,
    QR_MENU_BTNS,
    QR_SEND_BTNS,
)
from app.bot.keyboards.main_menu_kb import get_image_and_kb
from app.bot.keyboards.qr_menu_kb import get_trade_confirm_kb


from app.core.config import QR_DIR
from app.core.logging import get_logger
from app.bot.banners import captions, get_img
from app.sale_codes.dao import Sale_CodesDAO
from app.trades.dao import TradesDAO


async def get_qr_menu(
    level: int, menu_name: str, user_id: int, point_id: int, trade_id
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """Получить пользовательское меню."""
    match level:
        case 1:
            menu_name = QR_MENU
            btns_data = QR_MENU_BTNS
            caption = NO_CAPTION
            previous_menu = MAIN_MENU
        case 2:
            btns_data = QR_MENU_BTNS
            caption = NO_CAPTION
            previous_menu = QR_MENU
            user_codes = await Sale_CodesDAO.get_actual_objs(
                attr_name="user_id", attr_value=user_id
            )
            if menu_name == DELETE_QR:
                caption, btns_data = await get_user_codes_data(
                    user_id, menu_name, DELETE_QR_BTN
                )
            elif menu_name == QR_UPDATE:
                pass

    return await get_image_and_kb(
        menu_name=menu_name,
        user_id=user_id,
        point_id=point_id,
        btns_data=btns_data,
        level=level,
        caption=caption,
        previous_menu=previous_menu,
    )


async def get_user_codes_data(
    user_id: int, menu_name: str, btn_text: str
) -> tuple[str, tuple[str, str] | None]:
    """Получить описание данные для кнопок.
    Запрос в бд по id пользователя, возвращает список кодов юзера.
    """
    print(user_id, menu_name, btn_text)
    user_codes = await Sale_CodesDAO.get_actual_objs(
        attr_name="user_id", attr_value=user_id
    )
    if user_codes:
        caption = captions.del_qr
        btns_data = tuple(
            (menu_name, btn_text.format(code.value)) for code in user_codes
        )
    else:
        caption = captions.no_qr_today
        btns_data = None

    return caption, btns_data
