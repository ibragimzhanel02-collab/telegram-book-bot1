from django.contrib import admin

from .models import (
    Genre,
    Author,
    Book,
    Favorite,
    UserQuery,
    UserMessage,
    Broadcast
)

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Favorite)
admin.site.register(UserQuery)
admin.site.register(Broadcast)

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'message',
        'created_at'
    )

    search_fields = (
        'username',
        'message'
    )

    list_filter = (
        'created_at',
    )
