from app.bot.constants import NOTIFICATION_MSG_TEXT
from app.bot.create_bot import bot
from app.core.logging import logger
from app.users.dao import UsersDAO


async def send_order_notification() -> None:
    """Функция для уведомления пользователя о наличии заказов."""
    # timedeltas = в разработке
    users_tg_id_list = await UsersDAO.get_telegram_id()
    for tg_id in users_tg_id_list:
        try:
            await bot.send_message(
                chat_id=tg_id,
                text=NOTIFICATION_MSG_TEXT,
            )
        except Exception:
            logger("пользователь заблокировал бота")
