from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView


class OrdersListView(LoginRequiredMixin, ListView):
    pass
    # login_url = 'users:login'
    # template_name = 'orders/list_files.html'

    # def get_queryset(self):
    #     return File.objects.filter(owner=self.request.user)
