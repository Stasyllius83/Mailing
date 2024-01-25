
from smtplib import SMTPException
from django.core.mail import send_mail
from config import settings
from mailing.models import Log, MailingSettings
from django.utils import timezone


def send_mailling(mailing):
    current_time = timezone.localtime(timezone.now())
    if mailing.start_time <= current_time < mailing.end_time:
        for message in mailing.messages.all():
            for client in mailing.clients.all():
                try:
                    result = send_mail(
                        subject=message.title,
                        message=message.text,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False
                    )
                    log = Log.objects.create(
                        time=mailing.start_time,
                        status=result,
                        server_response='OK',
                        mailing_list=mailing,
                        client=client
                    )
                    log.save()
                    return log
                except SMTPException as error:
                    log = Log.objects.create(
                        time=mailing.start_time,
                        status=False,
                        server_response=error,
                        mailing_list=mailing,
                        client=client
                    )
                    log.save()
                return log
    else:
        mailing.status = MailingSettings.COMPLETED
        mailing.save()


def daily_mailings():
    mailings = MailingSettings.objects.filter(periodicity="Раз в день", status="Запущена")
    if mailings.exists():
        for mailing in mailings:
            send_mailling(mailing)


def weekly_mailings():
    mailings = MailingSettings.objects.filter(periodicity="Раз в неделю", status="Запущена")
    if mailings.exists():
        for mailing in mailings:
            send_mailling(mailing)


def monthly_mailings():
    mailings = MailingSettings.objects.filter(periodicity="Раз в месяц", status="Запущена")
    if mailings.exists():
        for mailing in mailings:
            send_mailling(mailing)
