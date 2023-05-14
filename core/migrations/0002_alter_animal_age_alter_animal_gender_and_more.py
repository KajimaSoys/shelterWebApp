# Generated by Django 4.2 on 2023-05-11 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='age',
            field=models.PositiveIntegerField(blank=True, help_text='Введите возраст животного в месяцах', null=True, verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Самец'), ('female', 'Самка'), ('unknown', 'Неизвестно')], max_length=255, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='weight',
            field=models.FloatField(blank=True, help_text='Введите вес животного в граммах', null=True, verbose_name='Вес'),
        ),
        migrations.AlterField(
            model_name='shelter',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]