import telebot
import os
import django
import random
import time
import schedule
import threading


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookbot.settings')
django.setup()

from books.models import Genre, Book, Author, Favorite, User, UserQuery, UserMessage, Broadcast
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8717776406:AAEbNW9ABxlsDvJdqPDzimU14EZPX6qhOAU"

bot = telebot.TeleBot(TOKEN)

def edit_or_send(call, text, markup=None):

    try:

        bot.edit_message_text(
            text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

    except:

        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=markup
        )


# ГЛАВНОЕ МЕНЮ

def main_menu():
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("📚 Жанры", callback_data="genres")
    )

    markup.add(
        InlineKeyboardButton("⭐ Избранное", callback_data="favorites")
    )
    markup.add(
        InlineKeyboardButton(
            "💳 Premium",
            callback_data="premium"
        )
    )

    return markup


# ОТПРАВКА КНИГИ

def send_book(chat_id, book):

    text = f"""
📖 {book.title}

👨‍💻 Автор: {book.author.name}

⭐ Рейтинг: {book.rating}

📌 Описание:
{book.description}
"""

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            "⭐ В избранное",
            callback_data=f"fav_{book.id}"
        )
    )


    bot.send_message(
        chat_id,
        text,
        reply_markup=markup
    )


#START

@bot.message_handler(commands=['start'])
def start(message):

    UserQuery.objects.create(
        user_id=message.from_user.id,
        username=message.from_user.username,
        message="/start"
    )

    user_exists = User.objects.filter(
        telegram_id=message.from_user.id
    ).first()

    if not user_exists:

        User.objects.create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name
        )

    bot.send_message(
        message.chat.id,
        """
        Добро пожаловать в Book Bot!
        Я помогу подобрать книги по жанрам и авторам

        Что умеет бот:

        📚 Рекомендации книг
        👨‍💻 Поиск по авторам
        🎲 Случайные книги
        ⭐ Избранное
        💳 Premium

        Выберите действие ниже 👇
        """
        ,
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['help'])
def help_command(message):

    text = """
📚 Book Bot Help

Доступные команды:

/start — запуск бота

/help — помощь

Функции бота:

📚 Выбор книг по жанрам

👨‍💻 Поиск по авторам

🎲 Случайная книга

⭐ Избранное

📢 Рассылки

⏰ Напоминания

💳 Premium раздел
"""

    bot.send_message(
        message.chat.id,
        text
    )


# ГЛАВНОЕ МЕНЮ

@bot.callback_query_handler(func=lambda call: call.data == "home")
def home(call):

    edit_or_send(
        call,
        "🏠 Главное меню",
        main_menu()
    )


#ЖАНРЫ

@bot.callback_query_handler(func=lambda call: call.data == "genres")
def genres(call):

    markup = InlineKeyboardMarkup()

    for g in Genre.objects.all():

        markup.add(
            InlineKeyboardButton(
                g.name,
                callback_data=f"genre_{g.id}"
            )
        )

    markup.add(
        InlineKeyboardButton(
            "⬅️ Главное меню",
            callback_data="home"
        )
    )

    edit_or_send(
        call,
        "📚 Выберите жанр:",
        markup
    )

#МЕНЮ ЖАНРА

@bot.callback_query_handler(func=lambda call: call.data.startswith("genre_"))
def genre_menu(call):

    genre_id = call.data.split("_")[1]

    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            "🎲 Рандомная книга",
            callback_data=f"random_{genre_id}"
        )
    )

    markup.add(
        InlineKeyboardButton(
            "👨‍💻 Авторы",
            callback_data=f"authors_{genre_id}"
        )
    )

    markup.add(
        InlineKeyboardButton(
            "⬅️ Назад",
            callback_data="genres"
        )
    )

    edit_or_send(
        call,
        "📖 Что хотите посмотреть?",
        markup
    )


# РАНДОМНАЯ КНИГА

@bot.callback_query_handler(func=lambda call: call.data.startswith("random_"))
def random_book(call):

    genre_id = call.data.split("_")[1]

    books = Book.objects.filter(
        author__genre_id=genre_id
    )

    if books:

        book = random.choice(list(books))

        send_book(
            call.message.chat.id,
            book
        )


# АВТОРЫ

@bot.callback_query_handler(func=lambda call: call.data.startswith("authors_"))
def authors(call):

    genre_id = call.data.split("_")[1]

    markup = InlineKeyboardMarkup()

    for a in Author.objects.filter(genre_id=genre_id):

        markup.add(
            InlineKeyboardButton(
                a.name,
                callback_data=f"author_{a.id}"
            )
        )

    markup.add(
        InlineKeyboardButton(
            "⬅️ Назад",
            callback_data=f"genre_{genre_id}"
        )
    )

    edit_or_send(
        call,
        "👨‍💻 Выберите автора:",
        markup
    )


# КНИГИ АВТОРА

@bot.callback_query_handler(func=lambda call: call.data.startswith("author_"))
def books_by_author(call):

    author_id = call.data.split("_")[1]

    markup = InlineKeyboardMarkup()

    books = Book.objects.filter(author_id=author_id)

    for b in books:

        markup.add(
            InlineKeyboardButton(
                b.title,
                callback_data=f"book_{b.id}"
            )
        )

    markup.add(
        InlineKeyboardButton(
            "⬅️ Назад",
            callback_data="genres"
        )
    )

    edit_or_send(
        call,
        "📚 Книги автора:",
        markup
    )


# ИНФОРМАЦИЯ О КНИГЕ

@bot.callback_query_handler(func=lambda call: call.data.startswith("book_"))
def book_info(call):

    book_id = call.data.split("_")[1]

    book = Book.objects.get(id=book_id)

    send_book(
        call.message.chat.id,
        book
    )


# ДОБАВИТЬ В ИЗБРАННОЕ

@bot.callback_query_handler(func=lambda call: call.data.startswith("fav_"))
def add_fav(call):

    book_id = call.data.split("_")[1]

    already_exists = Favorite.objects.filter(
        user_id=call.from_user.id,
        book_id=book_id
    ).first()

    if already_exists:

        bot.answer_callback_query(
            call.id,
            "⚠️ Уже в избранном"
        )

        return

    Favorite.objects.create(
        user_id=call.from_user.id,
        book_id=book_id
    )

    bot.answer_callback_query(
        call.id,
        "⭐ Добавлено в избранное!"
    )


# ИЗБРАННОЕ

@bot.callback_query_handler(func=lambda call: call.data == "favorites")
def favorites(call):

    favs = Favorite.objects.filter(
        user_id=call.from_user.id
    )

    if not favs:

        bot.send_message(
            call.message.chat.id,
            "❌ Избранных книг пока нет"
        )

        return

    for f in favs:

        send_book(
            call.message.chat.id,
            f.book
        )



def check_broadcasts():

    broadcasts = Broadcast.objects.filter(sent=False)

    users = UserMessage.objects.values_list(
        'user_id',
        flat=True
    ).distinct()

    for broadcast in broadcasts:

        for user_id in users:

            try:
                bot.send_message(
                    user_id,
                    f"📢 {broadcast.text}"
                )
            except Exception as e:
                print(e)


        broadcast.sent = True
        broadcast.save()


@bot.callback_query_handler(func=lambda call: call.data == "premium")
def premium(call):

    text = """
💎 PREMIUM ПОДПИСКА

✅ Безлимитные рекомендации
✅ Эксклюзивные книги
✅ Личный список чтения

💳 Оплата временно недоступна
"""

    bot.send_message(
        call.message.chat.id,
        text
    )
def reminder_message():

    users = UserMessage.objects.values_list(
        'user_id',
        flat=True
    ).distinct()

    for user in users:

        try:
            bot.send_message(
                user,
                "📚 Не забудьте почитать сегодня!"
            )
        except:
            pass


schedule.every().day.at("18:50").do(reminder_message)

# ЗАПУСК

print("Бот запущен...")


@bot.message_handler(func=lambda message: True)
def chat_dialog(message):

    if not message.text:

        bot.send_message(
            message.chat.id,
            "❌ Пустое сообщение"
        )

        return

    text = message.text.lower()

    # сохранение сообщений

    UserMessage.objects.create(
        user_id=message.from_user.id,
        username=message.from_user.username,
        message=message.text
    )

    # приветствие

    if text in ["привет", "hello", "hi"]:

        bot.send_message(
            message.chat.id,
            "👋 Привет! Я бот рекомендаций книг 📚"
        )

    # помощь

    elif text in ["помощь", "help"]:

        bot.send_message(
            message.chat.id,
            "❓ Используй /help"
        )

    # рекомендации

    elif "книга" in text:

        bot.send_message(
            message.chat.id,
            "📚 Используйте кнопку Жанры для выбора книг"
        )

    # авторы

    elif "автор" in text:

        bot.send_message(
            message.chat.id,
            "👨‍💻 Выберите жанр → автор → книгу"
        )

    # избранное

    elif "избранное" in text:

        bot.send_message(
            message.chat.id,
            "⭐ Откройте раздел Избранное"
        )

    # рейтинг

    elif "рейтинг" in text:

        bot.send_message(
            message.chat.id,
            "⭐ У каждой книги есть рейтинг"
        )

    # жанры

    elif "жанр" in text:

        bot.send_message(
            message.chat.id,
            "📚 Доступно более 10 жанров"
        )

    # premium

    elif "premium" in text:

        bot.send_message(
            message.chat.id,
            "💳 Premium раздел доступен в меню"
        )

    # погода

    elif text.startswith("/weather"):

        bot.send_message(
            message.chat.id,
            "🌤 Функция погоды пока в разработке"
        )

    # неизвестная команда

    else:

        bot.send_message(
            message.chat.id,
            "❌ Неизвестная команда\nИспользуйте /help"
        )


def check_admin_replies():

    messages = UserMessage.objects.filter(
        replied=False
    ).exclude(
        admin_reply__isnull=True
    ).exclude(
        admin_reply=""
    )

    for msg in messages:

        try:

            bot.send_message(
                msg.user_id,
                f"📩 Ответ поддержки:\n\n{msg.admin_reply}"
            )

            msg.replied = True

            msg.save()

        except:
            pass


def background_tasks():

    while True:

        schedule.run_pending()

        check_broadcasts()

        check_admin_replies()

        time.sleep(3)


threading.Thread(
    target=background_tasks,
    daemon=True
).start()


bot.infinity_polling(
    timeout=10,
    long_polling_timeout=5
)


# python bookbot/bot.py
#python bookbot/manage.py runserver
#http://127.0.0.1:8000/admin