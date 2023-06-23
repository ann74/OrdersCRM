from django.urls import path

from orders_app.apps import OrdersAppConfig
from orders_app.views import OrdersListView, AddOrderView, DetailOrderView, DeleteOrderView, UpdateOrderView,\
    TargetEmployer, order_completed, order_finished, HistoryOrdersListView


app_name = OrdersAppConfig.name

urlpatterns = [
    path('', OrdersListView.as_view(), name='list'),
    path('add_order/', AddOrderView.as_view(), name='add'),
    path('<int:pk>/', DetailOrderView.as_view(), name='detail'),
    path('<int:pk>/delete/', DeleteOrderView.as_view(), name='delete'),
    path('<int:pk>/update/', UpdateOrderView.as_view(), name='update'),
    path('<int:pk>/employer/', TargetEmployer.as_view(), name='employer'),
    path('<int:order_pk>/completed/', order_completed, name='complete'),
    path('<int:order_pk>/finished/', order_finished, name='finish'),
    path('history/', HistoryOrdersListView.as_view(), name='history'),

]
