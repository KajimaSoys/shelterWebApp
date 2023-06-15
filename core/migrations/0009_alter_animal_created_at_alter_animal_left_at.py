# Generated by Django 4.2 on 2023-06-15 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_animal_created_at_animal_left_at_animal_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Начало пребывания в приюте'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='left_at',
            field=models.DateField(blank=True, null=True, verbose_name='Окончание пребывания в приюте'),
        ),
    ]