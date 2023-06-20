from django.urls import path, include

from orders_app.apps import OrdersAppConfig
from orders_app.views import OrdersListView

# from users_app.views import UserRegister

app_name = OrdersAppConfig.name

urlpatterns = [
    path('', OrdersListView.as_view(), name='list')

]
