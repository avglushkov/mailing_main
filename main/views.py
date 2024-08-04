from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from main.models import Mailing, Client, Attempt, Message
from main.forms import MailingForm, ClientForm, MessageForm


class MailingListView(ListView):
    model = Mailing
    template_name = 'main/home.html'
    extra_context = {'title': 'Рассылки'}


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_form.html'
    success_url = reverse_lazy('main:home')
    extra_context = {'title': 'Новая рассылка'}

    def form_valid(self, form):

        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/mailing_form.html'
    success_url = reverse_lazy('main:home')
    extra_context = {'title': 'Изменение рассылки'}


class MailingDetailView(DetailView):
    model = Mailing
    # template_name = 'main/home.html'
    extra_context = {'title': 'Рассылкa'}


class MessageListView(ListView):
    model = Message
    extra_context = {'title': 'Сообщения'}


class ClientListView(ListView):
    model = Client
    extra_context = {'title': 'Клиенты'}


class AttemptListView(ListView):
    model = Attempt
    extra_context = {'title': 'Рассылки'}



class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    success_url = reverse_lazy('main:clients')
    extra_context = {'title': 'Новый клиент'}

    def form_valid(self, form):

        client = form.save()
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'main/message_form.html'
    success_url = reverse_lazy('main:messages')
    extra_context = {'title': 'Новое сообщение'}

    def form_valid(self, form):

        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    success_url = reverse_lazy('main:clients')
    extra_context = {'title': 'Изменение клиента'}


class ClientDetailView(DetailView):
    model = Client

    extra_context = {'title': 'Клиент'}

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'main/message_form.html'
    success_url = reverse_lazy('main:messages')
    extra_context = {'title': 'Изменение сообщения'}


class MessageDetailView(DetailView):
    model = Message

    extra_context = {'title': 'Сообщение'}