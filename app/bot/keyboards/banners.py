"""
Модуль для работы с изображениями и описаниям к ним.
"""

from aiogram.types import FSInputFile, InputMediaPhoto
import segno
from app.core.constants import FMT_JPG, FMT_PNG, NO_IMAGE
from app.bot.utils import generate_filename
from app.core.logging import logger
from app.core.config import QR_DIR, STATIC_DIR
from app.core.utils import decode_data, is_file_in_dir

BANNERS_DIR = STATIC_DIR / "banners"


async def get_img(
    menu_name: str,
    file_dir: str = BANNERS_DIR,
    caption: str = None,
    f_type: str = FMT_JPG,
) -> InputMediaPhoto:
    """
    Получить изображение с описанием.
    В функцию передаются имя меню и описание,
    если описания нет, то оно берется из класса Captions.
    Если нет необходимого изображения, то берется картинка 'no_image'.
    """
    if not caption:
        caption = getattr(captions, menu_name)
    media = await get_file(menu_name, file_dir, f_type)
    return InputMediaPhoto(media=media, caption=caption)


async def get_file(
    filename: str, file_dir: str = BANNERS_DIR, f_type: str = FMT_JPG
) -> FSInputFile:
    """Получить файл типа FSInputFile по имени в заданной директории."""
    if await is_file_in_dir(filename + f_type, file_dir):
        return FSInputFile(file_dir.joinpath(filename + f_type))
    return FSInputFile(file_dir.joinpath(NO_IMAGE + FMT_JPG))


async def get_qr_code_image(client_id: str, encoded_value: str):
    """
    Создать qr код.
    Создать файл с изображением и сохраняет, в дальнейшем
    он будет удален, после передачи в коллбэк.
    Возвращает InputMediaPhoto c изображением и описанием.
    """
    value = await decode_data(encoded_value)
    qr_data = "_".join((client_id, value))
    logger(qr_data)
    qr_img = segno.make_qr(qr_data)
    file_name = QR_DIR / ((await generate_filename()) + FMT_PNG)
    logger(file_name)
    qr_img.save(file_name, scale=10)
    mediaphoto = InputMediaPhoto(
        media=FSInputFile(file_name), caption=captions.confirm_trade
    )
    return mediaphoto


class Captions:
    choose_point = "Выберите нужный Вам пункт"
    confirm_trade = (
        "Оплачено - провести, НЕ оплачено - ОТКАЗ.\n\n"
        "Когда проведете заказ - нажмите 'ОК' для подтверждения "
        "и получения следующего кода."
    )
    registration_start = (
        "<b>Привет!  Я - бот обмена QR-кодами между менеджерами 😊</b>\n\n"
        "Давай пройдем простенькую регистрацию для нашей работы."
        "\n😜\n"
        "Вы готовы ответить на несколько вопросов?"
    )
    registration_done = (
        "Регистрация успешно пройдена! \n\n"
        "В разделе FAQ вы можете ознакомиться с возможностями бота."
    )
    main_menu = ""
    no_caption = ""
    no_image = ""
    no_registr = "Жаль, возвращайся, когда передумаешь."
    no_qr_today = "Нет загруженных QR кодов на сегодня. \n"
    not_found = (
        "Не удалось найти офис по предоставленным данным😕\n"
        "Проверьте их на корректность. \n\n"
        "Если верно - значит данный пункт отсутствует в бд, "
        "обратитесь к админу."
    )
    point_search = (
        "Введите адрес пункта (можно частично, но не меньше 5 букв) для его "
        "поиска, либо id пункта.\n\n"
        "Вы можете поочередно добавить до 10 пунктов."
    )
    qr_confirm = "✅ Заказ проведен ✅"
    qr_today = "Загруженные QR-коды"
    add_qr = (
        "Загрузите скриншот вашего кода, обрезав его, как показано выше.\n\n"
        "Изображение будет проверено🔎, пропускаются только 'правильные' "
        "скриншоты.\n\n"
        "Для отмены загрузки нажмите Назад"
    )
    point_no_qr = "На ваш пункт нет актуальных заказов. "
    no_user_point = (
        "Вы не назначили Ваш пункт. \n" "Это можно сделать в разделе Профиль"
    )
    search = "Поиск....дождитесь результата"
    qr_send = "Выберите id загруженного Вами кода."
    del_qr = (
        "Выберите код для удаления \n\n"
        "Также удаляться и созданные с ним трейды на другие пвз.\n\n"
        "Символ ⚠️ сигнализириует о том, что неоходимо загрузить новый qr, "
        "чтобы отправить трейды на другие пункты.\n\n"
        "Для обновления данных qr - просто загрузите новый "
        "в разделе <b>Загрузить код</b> - "
        "данные обновятся."
    )
    faq = (
        "Приветствую тебя в qr_trade боте\n\n"
        "Бот создан для быстрого обмена qr-кодами между менеджерами "
        "пунктов выдачи с целью поддержания рейтинга в идеальном состоянии.\n"
        "Выберите раздел, про который хотите узнать. \n\n"
        "P.S. Код писал на коленке, возможны косяки, баги. "
        "Есть вопросы, нашли баг и т.д - писать админу =)"
    )
    faq_profile = (
        "В меню профиля ты можешь посмотреть свои личные данные. "
        "При желании сменить пункт или вовсе его удалить, настроить "
        "уведомления. \n\nДоступны три режима <b>ВКЛ</b> (всегда), "
        "<b>ВЫКЛ</b> (отключены), <b>ПО ГРАФИКУ</b>.\n\n "
        "Для уведомлений по вашему рабочему графику необходимо "
        "установить свой рабочий график.\n\n"
        "В меню графика на клавиатуре будут кнопки с датами текущего месяца"
        " и плюс несколько дат соседних месяцев для создания полных недель."
        "\n\nВ момент заполнения не спамьте по клавиатуре слишком быстро, "
        "дайте телеграмму обработать запрос - выбранная вами дата после "
        "будет помечена на клавиатуре. Повторное нажатие на дату с пометкой "
        "уберет день из графика. \n\n"
        "После заполнения графика, нажмите кнопку <b>Сохранить график</b>\n"
        "Вам будут приходить сообщения о доступных кодах на ваш пункт только"
        " в те дни, когда вы работаете.\n\n"
        "Если отключить уведомления, запросить актуальный код можно "
        "будет через меню QR.\n\n"
    )
    faq_qr = (
        "Кнопка <b>Отправить QR</b> - загрузка скриншота кода. "
        "Изображения валидируются, всякий мусор с ссылками и прочее -"
        " не пройдет.\n\nОтправить их на целевые пункты по кнопке "
        "<b>отправить Код</b>.\nКнопка <b>Получить QR</b> делает запрос и "
        "проверяет, есть ли актуальные коды на ваш пункт. Можно использовать"
        " в любое время, даже если у вас уведомления в режиме ВКЛ(всегда)."
        "\n\nЕсли у вас назначен рабочий пункт - вам будут приходить "
        "уведомления о наличии кодов продаж на "
        "ваш пункт.\nМожно настроить уведомления по графику работы. В таком "
        "случае, уведомления будут приходить только в рабочие дни.\n\n"
        "Во избежание лишнего спама - уведомления приходят по часам, в 11, 14"
        ", 17, 20.\n\n"
        "Кнопка <b>Отправить QR</b> - открывает раздел поиска пункта выдачи. "
        "\nВы можете осуществлять поиск по адресу или по id пункта.\n"
        "В список на отправку можно добавить до 10 пунктов.\n\n"
        "Кнопка <b>Удалить QR</b> - удаление загруженного Вами кода, "
        "используйте, если загрузили код со старыми данными по ошибке."
        "\n\nВсе загруженные коды автоматически удаляются на следующий день."
    )

    def __getattr__(self, name):
        return self.no_caption


captions = Captions()
