from aiogram.filters.callback_data import CallbackData

from app.users.models import Users


class MenuCallBack(CallbackData, prefix="menu"):
    """
    Фабрика колбэков.

    level :: атрибут указывающий на глубину(шаг) меню.

    menu_name :: название меню.
    """

    level: int = 0
    menu_name: str
    user_id: int | None = None
    point_addres: str | None = None
    ok: str | None = None
    yes_no: str | None = None
