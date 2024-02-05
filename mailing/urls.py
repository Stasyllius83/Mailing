from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import ClientCreateView, ClientDeleteView, ClientListView, ClientUpdateView, \
    LogListView, MailingCreateView, MailingDeleteView, MailingDetailView, MailingListView, \
        MailingUpdateView, contact, toggle_active_client, toggle_active_mailing, HomeView
from django.views.decorators.cache import cache_page, never_cache

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(HomeView.as_view()), name='home'),
    path('clients/create', never_cache(ClientCreateView.as_view()), name='create_client'),
    path('clients/edit/<int:pk>/', never_cache(ClientUpdateView.as_view()), name='client_edit'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients', cache_page(60)(ClientListView.as_view()), name='clients_list'),
    path('create', never_cache(MailingCreateView.as_view()), name='create_mailing'),
    path('mailing/edit/<int:pk>/', never_cache(MailingUpdateView.as_view()), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_list', cache_page(60)(MailingListView.as_view()), name='mailing_list'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('log', cache_page(60)(LogListView.as_view()), name='log_list'),
    path("contact/", contact, name='contact'),
    path('set_active_client/<int:pk>', toggle_active_client, name='set_active_client'),
    path('mailing_set_active/<int:pk>', toggle_active_mailing, name='set_active'),
]
