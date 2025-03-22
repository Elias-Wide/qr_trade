# qr_trade BOT
# Телеграм-бот "qr_trade"

## Назначение:
Обмен qr-кодами для проведения заказов личных заказов для менеджеров wb.

Бот начинает с вводного приветствия и быстрый регистрации.
Пользователь может становить свой рабочий пункт, настроить уведомления о новых заказов на его пункт. Доступны три типа уведомлений - всегда, выкл, по графику.
В разделе профиля менеджер может установить рабочий график в рамках месяца.
Пользователь может загрузить qr-коды своих заказов(неограниченное количество), и отправить на другие пункты для проведения отказа или продажи и последующего выставления оценки пункту.

## Cтек:

![](https://img.shields.io/badge/Python-Version:_3.12.7-blue?logo=python&style=plastic)
![](https://img.shields.io/badge/FastAPI-Version:_0.115.7-blue?logo=fastapi&style=plastic)
![](https://img.shields.io/badge/Aiogram-Version:_3.17.0-blue?logo=fastapi&style=plastic)
![](https://img.shields.io/badge/SQLAlchemy-Version:_2.0.37-blue?logo=sqlalchemy&style=plastic)
![](https://img.shields.io/badge/Sqladmin-Version:_0.20.1-blue?logo=apscedule&style=plastic)
![](https://img.shields.io/badge/Pydantic-Version:_2.2.1-blue?logo=pydantic&style=plastic)
![](https://img.shields.io/badge/Alembic-Version:_1.14.1-blue?logo=alembic&style=plastic)
![](https://img.shields.io/badge/APScheduler-Version:_3.11.0-blue?logo=apscedule&style=plastic)
![](https://img.shields.io/badge/Pytz-Version:_2025.1-blue?logo=apscedule&style=plastic)
![](https://img.shields.io/badge/Uvicorn-Version:_0.34.0-blue?logo=uvicorn&style=plastic)


## Особенности проекта

Конфигурация проекта выполнена с использованием Pydantic_settings. Используется БД PostgreSQL. Миграции БД - alembic. Запросы - sqlalchemy.
Модуль бота - aiogram. Бот работает в режиме webhook с использованием жизненного цикла FastApi(lifespan).
Для выполнения функций по расписанию использован асинхронный APScheduler.
Админка создана с использованием SQLAdmin.
Работа с файлами qr-кодов осуществляется с помощью библиотек BytesIO (обработка файлов в буфере), pyzbar.
Работа с excel файлами для загрузки данных через бота - openpyxl.
Кодирование данных - Fernet (cryptography lib)

## Запуск проекта локально

- Склонируйте репозиторий и перейдите в директорию проекта

```shell
git clone \
git@github.com:Elias-Wide/qr_trade.git && \
cd qr_trade
```

- Установите и активируйте виртуальное окружение

```shell
python -m venv venv && source venv/Scripts/activate
```

- Установите зависимости

```shell
pip install -r requirements.txt
```

 - Запуск бота:

Локально запустить в режиме WEBHOOK не получится без установки ngrok, режим POLLING не предусмотрен. Установка наcтройка ngrok ( см. в интернет https://losst.pro/kak-polzovatsya-ngrok ) нужна для форвардинга порта localhost:8000 (FastAPI) в интернет с присвоением ему публичного динамического DNS имени.

* в файле main.env:

```text
db_host=localhost
db_name=qr_trade
db_port=5432
db_user=postgres
db_password=postgres

tg_bot_token=ВАШ_ТОКЕН_ТГ_БОТА
tg_admin_id=ваш телеграм id
tg_admin_username=ваш тг username
tg_webhook_host=полученнный url тоннеля ngrok (пример - https://c8f6-146-59-235-.ngrok-free.app)

app_admin_email=admin@email.ru
app_admin_password=adminpass 
app_logging_mode=on
app_secret_key="3X2l90dn6G3Jck9HG37GiqBeyBK-73hGDO7Mf4B18x4w="  Пример секретного ключа шифрования
app_admin_sc="642df74fkvpz8n6qa68e595de2bf25b" - пример секретного ключа для админки

```
Токен для админки можно сгенерировать с помощью библиотеки secrets, метод token_hex(32).
Токен для шифрования (app_secret_key) - сгенерировать с помощью Fernet.generate_key()
Полученный ключи записать в main.env.
Пример переменных окружения см. в main.env.example.

app_admin_email, app_admin_password для доступа в админку по адресу http://localhost:8000/admin.

Запускаем Ngrok
```shell
ngrok.exe http 8000
```

* Если БД не существует команда для создания:

```shell
alembic upgrade 661e97867c12  # это цифры последней ревизии 
```

* Cобственно запуск:

```shell
uvicorn app.main:app --reload 
```

## Запуск с использованием Docker.

* Скачиваем устанавливаем docker https://www.docker.com/
* Скачиваем устанавливаем ngrok.
* заполняем по скрипту выше файл main.env
* Дополнительно создается файл db.env 

```text
POSTGRES_DB=qr_trade
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_PORT=5432
```
* в файле main.env изменяем значение db_host на имя контейнера с базой db_host=postgres_main

* запускаем Docker compose:

```shell
docker compose up -build .
```

* в новом окне терминала применяем миграции
```shell
 docker compose exec main_bot alembic upgrade 661e97867c12  # это цифры последней ревизии 
```

* Остановить приложение (CTRL + C в терминале)
* Если docker compose запущен с флагом -d:

```shell
docker compose down
```

 ## Один из вариантов (простой деплой) на сервер (Ubuntu):

* Собираем образ и загружаем на DockerHuB
* Ngrok не нужен.
* На сервере в файлы main.env db.env заполняем как в примере с запуском Docker compose
* переносим на сервер в папку проекта(к файлам .env) docker-compose.production.yml
* в файле docker-compose.production.yml в сервисе main_bot, для image пишем имя вашего образа
* запускаем compose

```
sudo docker compose -f docker-compose.production.yml up -d
```
* Применяем миграции

```
sudo docker compose -f docker-compose.production.yml exec main_bot alembic upgrade 661e97867c12
````

* Для работы необходим публичный ip, либо  подключить домен.
  
Конфигурируем nginx, если используется. Пример в nginx.conf.example-no-ssl.
Дополнительгно получаем ssl сертификат.
Пример финальной конфигурации nginx в файле nginx.conf.example
Дополнительно необходимо добавить в файл конфигурации строчки 

```
add_header Content-Security-Policy upgrade-insecure-requests;
```

Это необходимо для правильной загрузки статики SQLAdmin.
* Перезагружаем nginx

````
sudo systemctl reload nginx
````
* Бот готов к работе!
  
Удачи!

## Автор
* [**Илья Широков**](https://github.com/Elias-Wide)
