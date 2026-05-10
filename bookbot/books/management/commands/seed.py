from django.core.management.base import BaseCommand
from books.models import Genre, Author, Book
import random

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        genres = [
            "Фантастика",
            "Детектив",
            "Роман",
            "Ужасы",
            "Фэнтези",
            "Научпоп",
            "История",
            "Психология",
            "Бизнес",
            "Приключения"
        ]

        for g in genres:

            genre = Genre.objects.create(name=g)

            for i in range(5):

                author = Author.objects.create(
                    name=f"{g} Автор {i+1}",
                    genre=genre
                )

                for j in range(2):

                    Book.objects.create(
                        title=f"{g} Книга {i+1}-{j+1}",
                        author=author,
                        description="Очень интересная книга",
                        rating=round(random.uniform(3, 5), 1)
                    )

        print("База заполнена!")