# Интернет-магазин *Megano*

**Megano** — полноценный интернет-магазин, разработанный в рамках дипломного проекта.  
Аналоги: holodilnik.ru, citilink.ru, ozon.ru.

## Технологический стек

- **Backend**: Django 5.x + Django REST Framework
- **Frontend**: HTML/CSS/JS (diploma-frontend — статические файлы + шаблоны)
- **База данных**: PostgreSQL 16
- **Зависимости**: Poetry 2.x
- **Веб-сервер**: Gunicorn (production) + collectstatic
- **Контейнеризация**: Docker + docker-compose

## Структура сайта

- **Главная страница** — топ-товары, популярные товары, limited edition
- **Каталог** — с фильтрами, сортировкой, поиском
  - Детальная страница товара (с отзывами)
- **Оформление заказа**
  - Корзина
  - Оформление заказа
  - Оплата
- **Личный кабинет**
  - Профиль
  - История заказов
- **Административный раздел** (Django Admin)
  - Управление товарами, категориями, заказами, скидками и т.д.

### Роли пользователей

- **Администратор** — полный доступ к админ-панели
- **Покупатель** — авторизованный пользователь (все публичные функции + заказы)
- **Гость** — просмотр каталога, сбор корзины (без оформления заказа)


## Требования к запуску

Проект **легкопереносимый**: достаточно клонировать репозиторий, настроить 
.enи запустить.

### Вариант 1 — Быстрый запуск через Docker (для демонстрации)

1. Клонируйте репозиторий  
   ```Bash
   git clone https://github.com/pigva91/megano-shop.git
   cd megano-shop
   
2. Создайте и заполните файл .env (пример указан в файле `.env.example`)

3. Запустите проект
   ```Bash
   docker compose up -d --build

4. Загрузите начальные данные (один раз)
   ```Bash
   docker compose exec app python manage.py loaddata fixtures/initial_data.json


Сайт доступен по адресу http://localhost:8000
Админка: http://localhost:8000/admin/
(логин: admin / пароль: 123456 из фикстур)

Остановка:
   ```Bash
   docker compose down
   ```

### Вариант 2 — Локальный запуск без Docker (для разработки)

1. Установите Poetry и зависимости
   ```Bash
   pip install poetry
   poetry install
   poetry shell

2. Создайте и настройте `.env` (см. выше, но DB_HOST=localhost)

3. Запустите PostgreSQL отдельно (можно через Docker)
   ```Bash
   docker compose up -d db

4. Миграции + данные
   ```Bash
   python manage.py migrate
   python manage.py loaddata fixtures/initial_data.json

5. Запуск
   ```Bash
   python manage.py runserver


### Тестовые данные

После загрузки `initial_data.json` доступны:

- **Администратор**: username `admin`, пароль `123456`
- **Тестовый покупатель**: username `test`, пароль `123456`
- **Категории**: Ноутбуки и компьютеры → Игровые ноутбуки, Смартфоны → 
  Аксессуары
- **Товары**: ASUS ROG Strix, iPhone 16 Pro, Samsung Galaxy S23 Ultra, MSI 
  Katana
- **Отзывы**, **скидки**, **спецификации**

### API (основные эндпоинты DRF)

- /api/sign-in/ — вход
- /api/sign-up/ — регистрация
- /api/profile/ — профиль
- /api/basket/ — корзина
- /api/orders/ — заказы
- /api/catalog/ — каталог
- /api/product/<id>/ — товар
- /api/payment/<id>/ — оплата
