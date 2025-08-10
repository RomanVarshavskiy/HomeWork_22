# Django Project: Skystore (chapter 6)

Небольшое учебное Django‑приложение с модулем `catalog`, в котором реализованы:
- главная страница каталога
- страница контактов с простой обработкой формы отправки сообщения

## Технологии
- Python 3.13
- Django 5.2
- Poetry (управление зависимостями и окружением)
- Инструменты качества кода: Black, isort, Flake8, MyPy

## Быстрый старт

1) Клонирование и установка зависимостей
powershell
# Windows PowerShell
poetry install --with lint --no-root
Примечание: флаг `--no-root` устанавливает только зависимости, без попытки устанавливать сам проект как пакет. Это удобно для типичного Django‑приложения.

2) Переменные окружения  
Скопируйте файл `.env_template` в `.env` и заполните значения:
bash
# .env
DJANGO_SECRET_KEY=your_secret_key_here DJANGO_DEBUG=True

3) Миграции и запуск сервера разработки
powershell poetry run python manage.py migrate poetry run python manage.py runserver
Сервер будет доступен по адресу http://127.0.0.1:8000/

## Полезные URL
- Главная (каталог): `/`
- Контакты: `/contacts/`

## Структура (упрощённо)
. ├── catalog/ # Приложение каталога (urls, views, templates) ├── manage.py # Точка входа Django ├── pyproject.toml # Зависимости и настройки Poetry/линтеров ├── .env_template # Шаблон переменных окружения └── templates/ ├── home.html └── contacts.html


## Лицензия
Добавьте информацию о лицензии в этот раздел (например, MIT). Если лицензии нет — опишите условия использования проекта.
