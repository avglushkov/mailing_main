from django.db import models
from users.models import User


# Create your models here.

class Client(models.Model):
    email = models.EmailField(verbose_name='Электронная почта')
    full_name = models.CharField(max_length=100, verbose_name='ФИО клиента')
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.email} - {self.full_name}'


class Mailing(models.Model):
    name = models.CharField(max_length=100, verbose_name='Краткое наименование рассылки')
    first_sending = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время первой рассылки')
    last_sending = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время последней отправки рассылки')
    next_sending = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время следующей отправки рассылки')

    periodicity = models.CharField(max_length=20, choices=[('daily', 'раз в день'), ('weekly', 'раз в неделю'),
                                                           ('monthly', 'раз в месяц')], default='daily',
                                   verbose_name='Периодичность рассылки')
    status = models.CharField(max_length=10,
                              choices=[('new', 'создана'), ('finished', 'завершена'), ('started', 'запущена')],
                              default='new', verbose_name='Статус рассылки')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты для рассылки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.name


class Message(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    subject = models.CharField(max_length=100, verbose_name='Тема сообщения')
    body = models.TextField(verbose_name='Тело сообщения')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.subject} - {self.mailing}'


class Attempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    attempt_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время последней рассылки')
    status = models.CharField(max_length=15, blank=True, null=True,
                              choices=[('success', 'успешно'), ('unsuccess', 'не успешно')],
                              verbose_name='Статус попытки')
    server_answer = models.CharField(max_length=200, blank=True, null=True, verbose_name='Ответ сервера')

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'

    def __str__(self):
        return f'{self.attempt_date} - {self.mailing} - {self.status}'


