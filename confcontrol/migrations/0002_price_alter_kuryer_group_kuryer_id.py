# Generated by Django 4.0.1 on 2022-04-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confcontrol', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.IntegerField(verbose_name='Цена пункта A')),
                ('b1', models.IntegerField(verbose_name='Цена пункта B(0.1-5 Кг)')),
                ('b2', models.IntegerField(verbose_name='Цена пункта B(5.1-10 Кг)')),
                ('b3', models.IntegerField(verbose_name='Цена пункта B(10.1-20 Кг)')),
                ('comis', models.IntegerField(verbose_name='Комиссия NesuVezu %')),
            ],
            options={
                'verbose_name': 'Настройки цены',
                'verbose_name_plural': 'Настройки цены',
            },
        ),
        migrations.AlterField(
            model_name='kuryer_group',
            name='kuryer_id',
            field=models.BigIntegerField(verbose_name='Group ID'),
        ),
    ]
