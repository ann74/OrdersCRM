from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, FormView

from orders_app.forms import CreateOrderForm, TargetEmployerForm
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