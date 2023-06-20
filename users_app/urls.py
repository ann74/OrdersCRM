from django.urls import path, include
from django.contrib.auth import views as auth_views

from users_app.apps import UsersAppConfig
# from users_app.views import UserRegister

app_name = UsersAppConfig.name

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
