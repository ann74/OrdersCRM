from django.contrib import admin

from orders_app.models import Category, Orders


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'master', 'category']

