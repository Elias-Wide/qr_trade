"""
Модуль для работы с изображениями и описаниям к ним.
"""

import os
from io import BytesIO
from PIL import Image
from aiogram.types import BufferedInputFile, FSInputFile, InputMediaPhoto
import qrcode
from app.bot.constants import FMT_JPG, NO_IMAGE
from app.core.logging import logger
from app.core.config import STATIC_DIR
from app.core.utils import decode_data, is_file_in_dir
from app.sale_codes.dao import Sale_CodesDAO

BANNERS_DIR = STATIC_DIR / "banners"


async def get_img(
    menu_name: str,
    file_dir: str = BANNERS_DIR,
    caption: str = None,
    f_type: str = FMT_JPG,
) -> InputMediaPhoto:
    """
    Получить изображение.
    В функцию передаются имя меню, уровень меню и описание,
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
    """Получить файл по имени в заданной директории."""
    if await is_file_in_dir(filename + f_type, file_dir):
        return FSInputFile(file_dir.joinpath(filename + f_type))
    return FSInputFile(file_dir.joinpath(NO_IMAGE + FMT_JPG))


async def get_qr_code_image(client_id: str, encoded_value: str):
    value = await decode_data(encoded_value)
    qr_data = "_".join((client_id, value))
    logger(qr_data)
    qr_img = qrcode.make(qr_data)
    buffer = BytesIO()
    qr_img.save(buffer)
    buffer.seek(0)
    return BufferedInputFile(buffer.getvalue(), filename=f"QR {client_id}")
    return InputMediaPhoto(media=img, caption=captions.confirm_trade)


# file_name = await download_file(message.photo[-1], QR_DIR)
# file = await bot.get_file(message.photo[-1].file_id)
# # image = BytesIO(file)
# img = Image.open(BytesIO(file))
# output = BytesIO()
# image.save(output, format="JPEG", optimize=True, quality=Quality)
# image.seek(0)


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
        "Вы можете поочередно добавить до 7 пунктов."
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
        "Также удаляться и созданные с ним трейды на другие пвз.\n"
        "Знак ⚠️ сигнализирует о том, что необходимо обновить QR\n\n"
        "Просто загрузите новый qr в разделе Загрузить код - "
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
        "уведомления. \nДоступны три режима <b>ВКЛ</b> (всегда), "
        "<b>ВЫКЛ</b> (отключены), <b>ПО ГРАФИКУ</b>.\n "
        "Для уведомлений по вашему рабочему графику необходимо "
        "установить свой рабочий график.\n"
        "В меню графика на клавиутуре будут кнопки с датами текущего месяца"
        " и плюс несколько дат соседних месяцев для создания полных недель.\n"
        "В момент заполнения не спамьте по клавиатуре слишком быстро,"
        "дайте телеграмму обработать запрос - выбранная вами дата после "
        "будет помечена на клавиатуре. Повторное нажатие на дату с пометкой "
        "уберет день из графика. \n"
        "После заполнения графика, нажмите кнопку <b>Сохранить график</b>\n"
        "Вам будут приходить сообщения о доступных кодах на ваш пункт только "
        "в те дни, когда вы работаете.\n"
        "Если отключить уведомления, запросить актуальный код можно "
        "будет через меню QR.\n\n"
    )
    faq_qr = (
        "В данном разделе вы можете загрузить/удалить ваши QR коды, а после "
        "отправить их на целевые пункты по кнопке <b>отправить Код</b>.\n"
        "В список на отправку можно добавить до 7 пунктов, есть поиск по id и"
        " адресу.\n"
        "Кнопка 'Получить QR' делает запрос и проверяет, есть ли актуальные "
        "коды на ваш пункт. Можно использовать в любое время, даже если у вас"
        " уведомления в режиме 'ВКЛ'(всегда).\n Если у вас назначен рабочий "
        "пункт - вам будут приходить уведомления о наличии кодов продаж на "
        "ваш пункт.\nМожно настроить уведолмения по графику работы. В таком "
        "случае, уведомления будуn приходить только в рабочие дни.\n"
        "Во избежание лишнего спама - уведомления приходят по часам, в 11, 14"
        ", 17, 20.\n"
        "Кнопка <b>Отправить QR</b> - открывает раздел поиска пункта выдачи. \n"
        "Вы можете выбрать поиск по адресу или по id пункта\n"
        "Кнопка <b>Удалить QR</b> - удаление загруженного Вами кода, используйте, "
        "если загрузили код со старыми данными или по ошибке.\n\n"
        "Все загруженные коды автоматически удаляются на следующий день."
    )

    def __getattr__(self, name):
        return self.no_caption


captions = Captions()
