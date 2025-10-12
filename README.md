# Django Project: Romstore (chapter 6)

Небольшое учебное Django‑приложение, состоящее из модулей:

- catalog — витрина каталога с товарами и категориями (список, карточка, CRUD, загрузка изображений)
- myblog — простой блог (список, деталка со счетчиком просмотров и уведомлением, CRUD, загрузка превью)

Дополнительно:

- заготовка данных для каталога (через фикстуру и/или management‑команду)
- админ-панель для управления сущностями проекта

## Технологии

- Python 3.13
- Django 5.2
- Poetry (управление зависимостями и окружением)
- Инструменты качества кода: Black, isort, Flake8, MyPy

## Требования

- Установленный Python 3.13
- Установленный Poetry
- База данных по умолчанию — SQLite (ничего дополнительно настраивать не нужно)

## Быстрый старт

1) Клонирование и установка зависимостей

powershell

# Windows PowerShell

poetry install --with lint --no-root
Примечание: флаг `--no-root` устанавливает только зависимости, без попытки устанавливать сам проект как пакет. Это
удобно для типичного Django‑приложения.

2) Переменные окружения  
   Скопируйте файл `.env_template` в `.env` и заполните значения:

- Windows PowerShell:
  powershell Copy-Item .env_template .env
- macOS/Linux:
  bash cp .env_template .env
  Откройте `.env` и заполните значения:

dotenv SECRET_KEY=your_secret_key_here DEBUG=True NAME=your_name_her
Дополнительно при необходимости:
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=user@example.com
EMAIL_HOST_PASSWORD=your_password
EMAIL_PORT=587
EMAIL_USE_TLS=True

3) Миграции и запуск сервера разработки
   powershell poetry run python manage.py migrate poetry run python manage.py runserver
   Сервер будет доступен по адресу http://127.0.0.1:8000/

4) (Опционально) Создание суперпользователя для входа в админ‑пан
   poetry run python manage.py createsuperuser

5) (Опционально) Предзаполнение базы данных тестовыми данными

Вариант A — загрузка из фикстуры:
poetry run python manage.py loaddata catalog_fixture.json

Вариант B — через специальную management‑команду:
poetry run python manage.py add_products

## Полезные URL

- Главная (каталог): `/`
- Контакты: `/contacts/`
- Админ‑панель: `/admin/`
- Блог: `/blog/` (список публикаций), детальная страница — по ссылкам со списка

Примечания:

- В разработке медиа‑файлы (изображения) из каталога и блога отдаются из директории `media/`.
- В блоге реализован счётчик просмотров; при достижении порога отправляется письмо (настройте параметры email‑отправки в
  `.env`, либо используйте консольный backend, если задан в настройках проекта).

## Команды качества кода

- Форматирование:
  poetry run isort . poetry run black .

- Линтинг:
  poetry run flake8

- Статическая типизация:
  poetry run mypy .

Настройки инструментов сконфигурированы в `pyproject.toml`.

## Структура (упрощённо)

. ├── catalog/ # Приложение каталога (модели, вьюхи, формы, urls, шаблоны) │ ├── management/ # Команды управления (в
т.ч. add_products) │ ├── templates/catalog/ # Шаблоны каталога (список/деталка/формы/удаление и т.д.) │ └── ... ├──
myblog/ # Приложение блога (модели, вьюхи, urls, шаблоны) │ └── templates/myblog/ ├── config/ # Настройки проекта (
settings, urls, wsgi, asgi) ├── media/ # Загружаемые файлы (dev) ├── static/ # Статические файлы (если используются) ├──
catalog_fixture.json # Фикстура с тестовыми данными ├── .env_template # Шаблон переменных окружения ├── manage.py #
Точка входа Django ├── pyproject.toml # Зависимости и настройки Poetry/линтеров └── README.md

## Лицензия

