# Generated by Django 4.2 on 2023-05-11 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_animal_age_alter_animal_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Возраст(месяцы)'),
        ),
        migrations.AlterField(
            model_name='animal',
            name='weight',
            field=models.IntegerField(blank=True, null=True, verbose_name='Вес(граммы)'),
        ),
    ]
