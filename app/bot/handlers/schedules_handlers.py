from app.users.dao import UsersDAO


# async def time_to_send_notification() -> None:
#     """Функция для уведомления пользователя о наличии заказов."""
#     timedeltas = await get_timedeltas_from_constant_time(
#         TIME_CALORIES_FOR_SCHEDULER,
#     )
#     users_tg_id_list = await UsersDAO.get_telegram_id(
#         timedelta=timedeltas,
#     )
#     for tg_id in users_tg_id:
#         try:
#             await main.bot.send_message(
#                 chat_id=tg_id,
#                 text=TEXT_FOR_DIET_SIMPLE,
#                 reply_markup=get_remind_button(DIET),

#             )
#         except Exception:
#             logger.info('пользователь заблокировал бота')
