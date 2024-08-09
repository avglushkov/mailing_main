import random
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from main.models import Mailing, Client, Attempt, Notification
from main.forms import MailingForm, ClientForm, NotificationForm, MailingActivationForm
from blog.models import Blog


class MainPage(TemplateView):
    """Вывод главной страницы"""
    extra_context = {'title': 'Главная'}

    def get(self, request, *args, **kwargs):
        """Формирование контента главной страницы"""
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)

        context = {
            'title': 'Главная',
            'users_mailings': Mailing.objects.count(),
            'active_mailings': Mailing.objects.filter(is_active=True).count(),
            'clients': Client.objects.all().distinct('email').count(),
            'blog_list': blog_list[:3]
        }
        return render(request, 'main/home.html', context)


class MailingListView(LoginRequiredMixin,  ListView):
    """Вывод списка рассылок"""
    model = Mailing
    template_name = 'main/mailing_list.html'
    # permission_required = ('main.can_disable_mailings' or 'main.view_mailing')
    extra_context = {'title': 'Рассылки'}


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Новая рассылка"""
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_form.html'
    success_url = reverse_lazy('main:mailings')
    extra_context = {'title': 'Новая рассылка'}

    def form_valid(self, form):
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение рассылки"""
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_form.html'
    success_url = reverse_lazy('main:mailings')
    extra_context = {'title': 'Изменение рассылки'}


class MailingDetailView(DetailView):
    """Детализация рассылки"""

    model = Mailing
    template_name = 'main/mailing_detail.html'
    extra_context = {'title': 'Рассылкa'}


class MailingActivationView(LoginRequiredMixin, UpdateView):
    """Активация или деактивация рассылки"""

    model = Mailing
    template_name = 'main/mailing_activation.html'
    form_class = MailingActivationForm
    success_url = reverse_lazy("main:mailings")
    extra_context = {'title': 'Отключение / Подключение рассылки'}


class NotificationListView(ListView):
    """Вывод списка сообщений"""

    model = Notification
    extra_context = {'title': 'Сообщения'}


class ClientListView(ListView):
    """Вывод списка клиентов"""

    model = Client
    extra_context = {'title': 'Клиенты'}



class ClientCreateView(LoginRequiredMixin, CreateView):
    """Новый клиент"""

    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    success_url = reverse_lazy('main:clients')
    extra_context = {'title': 'Новый клиент'}

    def form_valid(self, form):
        """Определение владельца"""
        client = form.save()
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)


class NotificationCreateView(LoginRequiredMixin, CreateView):
    """Новое сообщение"""
    model = Notification
    form_class = NotificationForm
    template_name = 'main/notification_form.html'
    success_url = reverse_lazy('main:notifications')
    extra_context = {'title': 'Новое сообщение'}

    def form_valid(self, form):
        notification = form.save()
        notification.owner = self.request.user
        notification.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение клиента"""

    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    success_url = reverse_lazy('main:clients')
    extra_context = {'title': 'Изменение клиента'}


class ClientDetailView(DetailView):
    """Детализация клиента"""

    model = Client
    extra_context = {'title': 'Клиент'}


class NotificationUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение сообщения"""

    model = Notification
    form_class = NotificationForm
    template_name = 'main/notification_form.html'
    success_url = reverse_lazy('main:notifications')
    extra_context = {'title': 'Изменение сообщения'}


class AttemptListView(ListView):
    """Вывод лога рассылок"""

    model = Attempt
    extra_context = {'title': 'Лог рассылок'}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class NotificationDetailView(DetailView):
    """Детализация сообщения"""
    model = Notification
    extra_context = {'title': 'Сообщение'}


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailings')
    extra_context = {'title': 'Удаление рассылки'}


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:clients')
    extra_context = {'title': 'Удаление клиента'}


class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Notification
    success_url = reverse_lazy('main:notifications')
    extra_context = {'title': 'Удаление сообщения'}
