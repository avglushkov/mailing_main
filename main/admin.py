from django.contrib import admin
from main.models import Client, Mailing, Notification, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'email')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'periodicity', 'status')

@admin.register(Notification)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk','mailing', 'subject')

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('pk','mailing')