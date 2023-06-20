from django.contrib.auth.models import User
from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.title}'


class Orders(models.Model):
    NEW = 'new'
    ASSIGNED = 'assigned'
    DONE = 'done'
    COMPLETED = 'completed'

    STATUSES = (
        (NEW, 'новый'),
        (ASSIGNED, 'назначен'),
        (DONE, 'выполнен'),
        (COMPLETED, 'завершен'),
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='клиент', related_name='client')
    master = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='мастер', **NULLABLE, related_name='master')
    title = models.CharField(max_length=250, verbose_name='Краткое описание')
    category = models.ForeignKey(Category, default='Другое', on_delete=models.SET_DEFAULT, verbose_name='Категория')
    description = models.TextField(verbose_name='Подробное описание', **NULLABLE)
    status = models.CharField(choices=STATUSES, default=NEW, max_length=10, verbose_name='статус')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.title}'

