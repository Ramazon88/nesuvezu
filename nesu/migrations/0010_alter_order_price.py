# Generated by Django 4.0.1 on 2022-05-16 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nesu', '0009_alter_order_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Сумма'),
        ),
    ]
