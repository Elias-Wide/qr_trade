from app.users.dao import UsersDAO
from app.users.models import Users
from app.bot.create_bot import bot


async def get_user_data(user_id: int) -> str:
    """Получить данные пользователя."""
    try:
        user = await UsersDAO.get_user_full_data(user_id)
        result = (
            f"Ваши данные 📂: \n\n"
            f"Юзернэйм 📱:    {user.username}\n"
            f"Рабочий ID 🔮:    {user.manager_id}\n"
            f"Адрес пункта 🏚:    {user.addres}\n"
            f"Помогли другим 💟:   0\n"
        )
        return result + f"ID пункта: {user.point_id}" if user.point_id != 1 else result
    except:
        return "Ошибка получения данных"


# async def get_img(
#     menu_name: str,
#     level: int | None = None,
#     utc_offset_hours: int | None = None,
# ) -> InputMediaPhoto:
#     """Получить изображение к сообщению.

#     Возвращает баннер, соответствующий названию меню и уровню,
#     а также описание к нему.

#     Args:
#         menu_name (str): название меню
#         level (int | None, optional): уровень меню
#         utc_offset_hours (int | None, optional): разница во времени от UTC

#     Returns:
#         InputMediaPhoto: изображение к разделу меню, включая описание
#     """
#     match menu_name:
#         case SleepMode.GO_TO_BED:
#             caption_text = go_to_bed_time(utc_offset_hours)
#         case SleepMode.WAKE_UP:
#             caption_text = wake_up_time(utc_offset_hours)
#         case SleepMode.DURATION:
#             caption_text = get_sleep_duration()
#         case SleepMode.STATISTIC:
#             caption_text = get_sleep_statistic_answer()
#         case _:
#             caption_text = (
#                 CAPTIONS[menu_name][level] if level else CAPTIONS[menu_name]
#             )

#     return InputMediaPhoto(
#         media=FSInputFile(STATIC_DIR.joinpath(menu_name + FMT_JPG)),
#         caption=caption_text,
#     )
