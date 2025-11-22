from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MyUser

# Добавляем поле с биографией
# к стандартному набору полей (fieldsets) пользователя в админке.
UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio',)}),
)

admin.site.register(MyUser, UserAdmin)