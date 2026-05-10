import telebot
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookbot.settings')
django.setup()

from books.models import Genre, Book, Author, Favorite
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8717776406:AAEbNW9ABxlsDvJdqPDzimU14EZPX6qhOAU"

bot = telebot.TeleBot(TOKEN)


# ===== ГЛАВНОЕ МЕНЮ =====

def main_menu():
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("📚 Жанры", callback_data="genres")
    )

    markup.add(
        InlineKeyboardButton("⭐ Избранное", callback_data="favorites")
    )

    return markup


# ===== ОТПРАВКА КНИГИ =====

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

    markup.add(
        InlineKeyboardButton(
            "⬅️ Назад",
            callback_data="genres"
        )
    )

    bot.send_message(
        chat_id,
        text,
        reply_markup=markup
    )


# ===== START =====

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "📚 Добро пожаловать в бот рекомендаций книг!",
        reply_markup=main_menu()
    )


# ===== ГЛАВНОЕ МЕНЮ =====

@bot.callback_query_handler(func=lambda call: call.data == "home")
def home(call):

    bot.send_message(
        call.message.chat.id,
        "🏠 Главное меню",
        reply_markup=main_menu()
    )


# ===== ЖАНРЫ =====

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

    bot.send_message(
        call.message.chat.id,
        "📚 Выберите жанр:",
        reply_markup=markup
    )


# ===== МЕНЮ ЖАНРА =====

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

    bot.send_message(
        call.message.chat.id,
        "📖 Что хотите посмотреть?",
        reply_markup=markup
    )


# ===== РАНДОМНАЯ КНИГА =====

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


# ===== АВТОРЫ =====

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

    bot.send_message(
        call.message.chat.id,
        "👨‍💻 Выберите автора:",
        reply_markup=markup
    )


# ===== КНИГИ АВТОРА =====

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

    bot.send_message(
        call.message.chat.id,
        "📚 Книги автора:",
        reply_markup=markup
    )


# ===== ИНФОРМАЦИЯ О КНИГЕ =====

@bot.callback_query_handler(func=lambda call: call.data.startswith("book_"))
def book_info(call):

    book_id = call.data.split("_")[1]

    book = Book.objects.get(id=book_id)

    send_book(
        call.message.chat.id,
        book
    )


# ===== ДОБАВИТЬ В ИЗБРАННОЕ =====

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


# ===== ИЗБРАННОЕ =====

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


# ===== ЗАПУСК =====

print("Бот запущен...")

bot.infinity_polling()