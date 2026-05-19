from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user_id = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

class UserQuery(models.Model):

    user_id = models.IntegerField()

    username = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.username}: {self.message}"

class UserMessage(models.Model):

    user_id = models.IntegerField()

    username = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    message = models.TextField()

    admin_reply = models.TextField(
        blank=True,
        null=True
    )

    replied = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.username}: {self.message}"

class Broadcast(models.Model):

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:30]