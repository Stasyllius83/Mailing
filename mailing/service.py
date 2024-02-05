from django.core.mail import send_mail
from config import settings
from mailing.models import Client, Log, MailingSettings
from django.core.cache import cache


def send_deactivate_email(user):
    send_mail(
        'Вас деактивировали',
        'Уважаемый пользователь, вас деактивировали. Обратитесь в поддержку, чтобы активироваться',
        settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


def get_cached_main():
    if settings.CACHE_ENABLED:
        key = 'mailing_list'
        mailing_list = cache.get(key)
        if mailing_list is None:
            mailing_list = MailingSettings.objects.all()
            cache.set(key, mailing_list)
    else:
        mailing_list = MailingSettings.objects.all()

    return mailing_list


def get_cached_client():
    if settings.CACHE_ENABLED:
        key = 'client_list'
        client_list = cache.get(key)
        if client_list is None:
            client_list = Client.objects.all()
            cache.set(key, client_list)
    else:
        client_list = Client.objects.all()

    return client_list


def get_cached_mailing():
    if settings.CACHE_ENABLED:
        key = 'mailing_list'
        mailing_list = cache.get(key)
        if mailing_list is None:
            mailing_list = MailingSettings.objects.all()
            cache.set(key, mailing_list)
    else:
        mailing_list = MailingSettings.objects.all()

    return mailing_list


def get_cached_log():
    if settings.CACHE_ENABLED:
        key = 'mailing_log'
        mailing_log = cache.get(key)
        if mailing_log is None:
            mailing_log = Log.objects.all()
            cache.set(key, mailing_log)
    else:
        mailing_log = Log.objects.all()

    return mailing_log
