from django.forms import ModelForm
from mailing.models import Message, MailingSettings, Client
from django import forms


class MailingForm(ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('start_time', 'finish_time', 'periodicity', 'clients', 'owner',)


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'text',)


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('FIO', 'email', 'comment',)
