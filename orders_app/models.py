from django.contrib.auth.models import User
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.title}'


class Orders(models.Model):
    NEW = 'новая'
    ASSIGNED = 'назначена'
    DONE = 'выполнена'
    COMPLETED = 'завершена'

    STATUSES = (
        (NEW, 'новая'),
        (ASSIGNED, 'назначена'),
        (DONE, 'выполнена'),
        (COMPLETED, 'завершена'),
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='клиент', related_name='client')
    master = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='мастер', **NULLABLE,
                               related_name='master')
    title = models.CharField(max_length=250, verbose_name='Краткое описание')
    category = models.ForeignKey(Category, default='Другое', on_delete=models.SET_DEFAULT, verbose_name='Категория')
    description = models.TextField(verbose_name='Подробное описание', **NULLABLE)
    status = models.CharField(choices=STATUSES, default=NEW, max_length=10, verbose_name='Статус')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    date_execution = models.DateField(verbose_name='Срок выполнения', **NULLABLE)
    date_completed = models.DateField(verbose_name='Дата завершения', **NULLABLE)

    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    phone = PhoneNumberField(verbose_name='Телефон')



    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.title}'
