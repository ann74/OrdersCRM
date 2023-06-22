from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from orders_app.forms import CreateOrderForm, TargetEmployerForm
from orders_app.models import Orders
from orders_app.templates.orders.services import get_user_role


class OrdersListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'orders/list_orders.html'
    model = Orders

    def get_queryset(self):
        queryset = super().get_queryset()
        query_string = self.request.GET.get('search')
        if query_string:
            queryset = queryset.filter(title__icontains=query_string)
        role = get_user_role(self.request)
        if role == 'client':
            queryset = queryset.filter(client=self.request.user)
        else:
            queryset = queryset.exclude(status='завершена')
            if role == 'master':
                queryset = queryset.filter(master=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['role'] = get_user_role(self.request)
        return context_data


class AddOrderView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateOrderForm
    template_name = 'orders/add_order.html'
    success_url = reverse_lazy('orders:list')
    success_message = 'Заявка успешно создана!'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = self.request.user
            order.save()

        return redirect(self.success_url)


class DetailOrderView(LoginRequiredMixin, DetailView):
    template_name = 'orders/order_detail.html'
    model = Orders

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        context_data['role'] = get_user_role(self.request)
        return context_data


class DeleteOrderView(SuccessMessageMixin, View):
    model = Orders
    success_url = reverse_lazy('orders:list')
    success_message = 'Заявка удалена!'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        order = Orders.objects.get(id=self.kwargs['pk'])
        order.delete()
        return redirect(self.success_url)


class UpdateOrderView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Orders
    form_class = CreateOrderForm
    template_name = 'orders/update_order.html'
    success_url = reverse_lazy('orders:list')
    success_message = 'Файл успешно обновлен!'


class TargetEmployer(View):
    model = Orders
    success_url = reverse_lazy('orders:list')

    def get(self, request, *args, **kwargs):
        form = TargetEmployerForm()
        return render(request, 'orders/target_employer.html', {'form': form})

    def post(self, request, *args, **kwargs):
        order = Orders.objects.get(id=self.kwargs['pk'])
        form = TargetEmployerForm(self.request.POST)
        if form.is_valid():
            order.master = form.cleaned_data['master']
            order.save()

        return redirect(self.success_url)
