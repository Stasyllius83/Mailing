# Generated by Django 4.2.6 on 2024-02-02 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=150, unique=True, verbose_name='почта')),
                ('FIO', models.CharField(max_length=150, verbose_name='ФИО')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
                'ordering': ('FIO',),
                'permissions': [('set_active_client', 'Can active client')],
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_try', models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')),
                ('status_try', models.BooleanField(verbose_name='статус попытки')),
                ('response_server', models.CharField(blank=True, null=True, verbose_name='ответ почтового сервера')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='время начала рассылки')),
                ('finish_time', models.DateTimeField(verbose_name='время окончания рассылки')),
                ('periodicity', models.CharField(choices=[('Раз в день', 'Раз в день'), ('Раз в неделю', 'Раз в неделю'), ('Раз в месяц', 'Раз в месяц')], max_length=100, verbose_name='периодичность рассылки')),
                ('status', models.CharField(choices=[('Создана', 'Создана'), ('Запущена', 'Запущена'), ('Завершена', 'Завершена')], default='Создана', max_length=100, verbose_name='статус рассылки')),
                ('clients', models.ManyToManyField(to='mailing.client', verbose_name='клиенты рассылки')),
            ],
            options={
                'verbose_name': 'настройки рассылки',
                'verbose_name_plural': 'настройки рассылки',
                'permissions': [('set_active', 'Can active mailing')],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='тема письма')),
                ('text', models.TextField(verbose_name='тело письма')),
                ('mailing_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailing.mailingsettings', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
    ]
