from django.urls import path, include
from django.views.decorators.cache import cache_page
from main.apps import MainConfig
from main.views import MailingListView, MailingDetailView, MessageListView, AttemptListView, ClientListView, \
    MailingCreateView, MailingUpdateView, ClientCreateView, MessageCreateView, ClientDetailView, ClientUpdateView, \
    MessageDetailView, MessageUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='home'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_detail/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client_detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message_detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),

]
