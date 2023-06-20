from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View

from users_app.forms import UserRegisterForm


class UserRegister(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserRegisterForm
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('orders:list')
        if form.errors.get('password2', None):
            form.errors['пароль'] = form.errors.pop('password2')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
