from aiogram.filters.callback_data import CallbackData


class MenuCallBack(CallbackData, prefix="menu"):
    """
    Фабрика колбэков.

    level :: атрибут указывающий на глубину(шаг) меню
    menu_name :: название меню
    user_id :: id пользователя в бд
    point_id :: id пункта пользователя (не pk в бд)
    code_id :: id(pk) объекта Sale_Codes
    trade :: id(pk) объекта Trades
    day :: дата, переданная в строковом формате
    """

    level: int = 0
    menu_name: str
    user_id: int | None = None
    point_id: int | None = None
    code_id: int | None = None
    trade_id: int | None = None
    day: str | None = None
    # page: int | None = None
