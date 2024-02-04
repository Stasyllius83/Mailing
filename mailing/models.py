from django.db import models
from config import settings

NULLABLE = {'null': True, 'blank': True}

class Client(models.Model):
    email = models.EmailField(max_length=150, verbose_name='почта', unique=True)
    FIO = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self) -> str:
        return f'{self.FIO} {self.email}'

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ('FIO',)
        permissions = [
            ('set_active_client', 'Can active client'),
        ]


class MailingSettings(models.Model):
    DAYLY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_CHOICES = [
        (DAYLY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name='время начала рассылки')
    finish_time = models.DateTimeField(verbose_name='время окончания рассылки')
    periodicity = models.CharField(max_length=100, verbose_name='периодичность рассылки', choices=PERIODICITY_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=CREATED, verbose_name='статус рассылки')
    is_active = models.BooleanField(default=True)
    clients = models.ManyToManyField(Client, verbose_name='клиенты рассылки')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self) -> str:
        return f'time: {self.start_time} - {self.finish_time} periodicity: {self.periodicity}, status: {self.status}'

    class Meta:
        verbose_name = 'настройки рассылки'
        verbose_name_plural = 'настройки рассылки'
        permissions = [
            ('set_active', 'Can active mailing'),
        ]


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='тема письма')
    text = models.TextField(verbose_name='тело письма')

    mailing_list = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='рассылка', related_name='messages', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Log(models.Model):
    time_try = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    status_try = models.BooleanField(verbose_name='статус попытки')
    response_server = models.CharField(verbose_name='ответ почтового сервера', **NULLABLE)

    mailing_list = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент рассылки', **NULLABLE)

    def __str__(self):
        return f'{self.time_try} - {self.status_try}'

    class Meta:
        verbose_name='лог'
        verbose_name_plural='логи'
