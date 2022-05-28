# Generated by Django 4.0.1 on 2022-04-19 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dispatcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispatcher_telegram_id', models.BigIntegerField(verbose_name='Диспетчер Telegram ID')),
                ('dispatcher_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Имя диспетчера')),
            ],
            options={
                'verbose_name': 'Диспетчер',
                'verbose_name_plural': 'Диспетчеры',
            },
        ),
        migrations.CreateModel(
            name='Kuryer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kuryer_telegram_id', models.BigIntegerField(verbose_name='Курьер Telegram ID')),
                ('kuryer_name', models.CharField(blank=True, default='', max_length=100, verbose_name='Имя курьера')),
                ('inwork', models.BooleanField(default=False, verbose_name='Работает?')),
            ],
            options={
                'verbose_name': 'Курьер',
                'verbose_name_plural': 'Курьеры',
            },
        ),
        migrations.CreateModel(
            name='Kuryer_came_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kuryer_id', models.BigIntegerField(verbose_name='Group ID')),
            ],
            options={
                'verbose_name': 'Группа пришла и ушла',
                'verbose_name_plural': 'Группа пришла и ушла',
            },
        ),
        migrations.CreateModel(
            name='Kuryer_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kuryer_id', models.BigIntegerField(verbose_name='Kuryer group ID')),
            ],
            options={
                'verbose_name': 'Заказы Telegram Группа',
                'verbose_name_plural': 'Заказы Telegram Группа',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.CharField(default='', max_length=512, verbose_name='Партнер')),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнеры',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop', models.CharField(default='', max_length=512, verbose_name='Магазин')),
                ('location', models.CharField(default='https://yandex.ru/maps/?pt=longitude,latitude&z=18&l=map', max_length=512, verbose_name='Локация')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confcontrol.partner', verbose_name='Партнер')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Имя оператора')),
                ('telegram_id', models.BigIntegerField(verbose_name='Оператор ID')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='confcontrol.partner', verbose_name='Партнер')),
            ],
            options={
                'verbose_name': 'Оператор',
                'verbose_name_plural': 'Операторы',
            },
        ),
    ]
