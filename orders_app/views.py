from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from orders_app.models import Orders


class OrdersListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'orders/list_orders.html'

    def get_queryset(self):
        print(self.request.user.groups.first())
        if self.request.user.groups.first().name == 'clients':
            queryset = Orders.objects.filter(client=self.request.user)
        elif self.request.user.groups.first().name == 'masters':
            queryset = Orders.objects.filter(master=self.request.user)
        else:
            queryset = Orders.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        print(self.request.user.groups.first())
        if self.request.user.groups.first().name == 'clients':
            context_data['role'] = 'client'
        elif self.request.user.groups.first().name == 'masters':
            context_data['role'] = 'master'
        else:
            context_data['role'] = 'dispatcher'
        return context_data

