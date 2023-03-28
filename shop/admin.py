from django.contrib import admin
from .models import *
# Register your models here.

class AdminGadgets(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'exist')  # Отображение полей
    list_display_links = ('id', 'name')  # Установка ссылок на атрибуты
    search_field = ('name',)  # Поиск по полям
    list_editable = ('price', 'exist')  # Изменяемое поле
    list_filter = ('exist',)  # Фильтры полей


admin.site.register(Gadget, AdminGadgets)  # (Модель, Форма Админки модели)
