from django.db import models
from django.urls import reverse
import appltech.settings as settings

# Модель БД для гаджета. Основные поля - Название, Описание, Цена, Изображение

class Gadget(models.Model):
    name = models.CharField(max_length=100, verbose_name='Модель')
    description = models.TextField(
        blank=False, verbose_name='Описание')
    price = models.FloatField(null=False, verbose_name='Цена')
    date_create = models.DateField(
        auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(
        auto_now=True, null=True, verbose_name='Дата изменения')
    photo = models.ImageField(
        upload_to=settings.MEDIA_ROOT, null=True, verbose_name='Фото')
    exist = models.BooleanField(
        default=True, verbose_name='На сайте?')

    def __str__(self):
        return f'Название: {self.name}\nЦена: {self.price} руб.\n'

    def __repr__(self):
        return f'Название: {self.name}\nЦена: {self.price} руб.\n'

    class Meta:
        verbose_name = 'Гаджет'
        verbose_name_plural = 'Гаджеты'


    # def get_absolute_url(self):
    #     return reverse('gadget_id', kwargs={'gadget_id': self.pk})