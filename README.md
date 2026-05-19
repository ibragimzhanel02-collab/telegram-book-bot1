# 📚 Telegram Book Bot

## Описание проекта

Telegram-бот для рекомендаций книг, разработанный на Python и Django.

Бот позволяет:

- выбирать книги по жанрам
- искать книги по авторам
- получать случайные рекомендации
- сохранять книги в избранное
- просматривать рейтинг и описание книг
- получать рассылки и напоминания

Также проект содержит Django-admin для управления пользователями и сообщениями.

---

## Используемые технологии

- Python
- Django
- SQLite
- pyTelegramBotAPI
- GitHub
- Schedule

---

## Установка

Клонировать проект:

```bash
git clone https://github.com/ibragim.zhamel02/telegram-book-bot1.git
```

Перейти в папку:

```bash
cd telegram-book-bot1
```

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Активировать:

Windows:

```bash
.venv\Scripts\activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

---

## Запуск

Запуск Django:

```bash
python bookbot/manage.py runserver
```

Запуск Telegram-бота:

```bash
python bookbot/bot.py
```

---

## Возможности

📚 Жанры книг

👨‍💻 Авторы

🎲 Рандомные книги

⭐ Избранное

📢 Массовая рассылка

⏰ Напоминания

💳 Premium раздел

📩 Ответ пользователям через Django Admin

---

## Скриншоты

### Telegram интерфейс

(вставить скрин главного меню)

### Django Admin

![img.png](img.png)
