# from aiogram.types import FSInputFile, InputMediaPhoto

# from app.core.config import STATIC_DIR


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