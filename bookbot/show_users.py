import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookbot.settings')
django.setup()

from books.models import User

users = User.objects.all()

for user in users:

    print(
        f"ID: {user.telegram_id} | "
        f"Имя: {user.first_name} | "
        f"Username: @{user.username}"
    )