from app.core.constants import EXPIRED, NOTIFICATION_MSG_TEXT
from app.bot.create_bot import bot
from app.core.logging import logger
from app.sale_codes.dao import SaleCodesDAO
from app.schedules.dao import SchedulesDAO
from app.trades.dao import TradesDAO
from app.trades.models import Trades
from app.users.dao import UsersDAO


async def send_order_notification() -> None:
    """Функция для уведомления пользователя о наличии заказов."""
    # timedeltas = в разработке
    users_tg_id_list = await UsersDAO.get_telegram_id_for_trades()
    logger(users_tg_id_list)
    for tg_id in users_tg_id_list:
        try:
            await bot.send_message(
                chat_id=tg_id,
                text=NOTIFICATION_MSG_TEXT,
            )
        except Exception:
            logger(f"Пользователь {tg_id} заблокировал бота")


async def expire_old_sale_codes() -> bool:
    """Функция для замены encoded_value модели SaleCodes на 'expired."""
    logger()
    sale_codes = await SaleCodesDAO.get_multi()
    for code in sale_codes:
        await SaleCodesDAO.update(code, {"encoded_value": EXPIRED})


async def delete_old_trades() -> bool:
    logger()
    return await delete_old_db_objs(TradesDAO)


async def delete_old_db_objs(modelDAO: TradesDAO | SaleCodesDAO) -> bool:
    """Удалить старые трейды."""
    return await modelDAO.delete_old_objs()


async def clear_user_schedule() -> None:
    """Очистить график пользователей в начале месяца."""
    await SchedulesDAO.clear_users_schedule()
