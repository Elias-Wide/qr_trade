from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.constants import MAIN_MENU, NO_CAPTION, QR_SEND, QR_UPDATE
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import CHECK_QR, DELETE_QR, QR_MENU, QR_MENU_BTNS, QR_SEND_BTNS
from app.bot.keyboards.main_menu_kb import get_image_and_kb
from app.bot.keyboards.qr_menu_kb import get_qr_delete_kb, get_trade_confirm_kb


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
            menu_name=QR_MENU
            btns_data = QR_MENU_BTNS
            caption = NO_CAPTION
            previous_menu = MAIN_MENU
            # return await get_image_and_kb(
            #     menu_name=QR_MENU,
            #     user_id=user_id,
            #     btns_data=QR_MENU_BTNS,
            #     caption=NO_CAPTION,
            #     level=level,
            #     point_id=point_id,
            # )
        case 2:
            menu_name=QR_MENU
            btns_data = QR_MENU_BTNS
            caption = NO_CAPTION
            previous_menu = MAIN_MENU
            if menu_name == DELETE_QR:
                user_codes = await Sale_CodesDAO.get_actual_objs(
                    attr_name="user_id", attr_value=user_id
                    )
                if not user_codes:
                    caption = captions.no_qr_today
                else:
                    caption = captions.del_qr
                return (
                    await get_img(menu_name, caption=caption),
                    await get_qr_delete_kb(user_id=user_id, level=level),
                )
            elif menu_name == QR_SEND:
                return await get_image_and_kb(
                    menu_name=QR_SEND,
                    user_id=user_id,
                    btns_data=QR_SEND_BTNS,
                    caption=captions.send_qr,
                    level=level,
                    point_id=point_id,
                )
            elif menu_name == QR_UPDATE:   
                pass
    return await get_image_and_kb(menu_name, user_id, point_id, btns_data, level, caption, previous_menu,)


async def get_actual_trade_answer(callback_data: MenuCallBack) -> tuple[InputMediaPhoto, InlineKeyboardMarkup] | None:
    """Получить актуальный объект модели trade для офиса(point).
    Возвращает клавиаутуру с и изображение для трейда."""
    trades_to_point = await TradesDAO.get_trades_by_point(callback_data.point_id)
    if trades_to_point:
        trade = trades_to_point[0]
        return (
            await get_img(menu_name=trade.file_name, file_dir=QR_DIR, caption=captions.confirm_trade.format(len(trades_to_point))),
            await get_trade_confirm_kb(level=callback_data.level, user_id=callback_data.user_id, point_id=callback_data.point_id, trade_id=trade.id)
        )
