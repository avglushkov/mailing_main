from django.urls import path, include
from django.views.decorators.cache import cache_page
from main.apps import MainConfig
from main.views import MailingListView, MailingDetailView, NotificationListView, AttemptListView, ClientListView, \
    MailingCreateView, MailingUpdateView, ClientCreateView, NotificationCreateView, ClientDetailView, ClientUpdateView, \
    NotificationDetailView, NotificationUpdateView, MainPage, MailingDeleteView, ClientDeleteView, \
    NotificationDeleteView, MailingActivationView

app_name = MainConfig.name

urlpatterns = [
    path('', MainPage.as_view(), name='home'),

    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_activation/<int:pk>/', MailingActivationView.as_view(), name='mailing_activation'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client_detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),

    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notification_create/', NotificationCreateView.as_view(), name='notification_create'),
    path('notification_update/<int:pk>', NotificationUpdateView.as_view(), name='notification_update'),
    path('notification_detail/<int:pk>', NotificationDetailView.as_view(), name='notification_detail'),
    path('notification/delete/<int:pk>', NotificationDeleteView.as_view(), name='notification_delete'),

    path('attempts/', AttemptListView.as_view(), name='attempts'),

]
