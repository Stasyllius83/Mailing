from django.contrib import admin

from mailing.models import Client, MailingSettings, Message

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'FIO', 'is_active', 'owner')
    list_filter = ('is_active','owner')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'finish_time', 'periodicity', 'status', 'is_active', 'owner')
    list_filter = ('periodicity','status', 'is_active')
    search_fields = ('periodicity','status')
    list_display_links = ['owner','periodicity','status']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text',)
