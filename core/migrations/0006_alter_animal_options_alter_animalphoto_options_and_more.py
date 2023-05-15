# Generated by Django 4.2 on 2023-05-15 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_shelter_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animal',
            options={'ordering': ['order'], 'verbose_name': 'Животное', 'verbose_name_plural': 'Животные'},
        ),
        migrations.AlterModelOptions(
            name='animalphoto',
            options={'ordering': ['order'], 'verbose_name': 'Фотография животного', 'verbose_name_plural': 'Фотографии животных'},
        ),
        migrations.AlterModelOptions(
            name='moneyreport',
            options={'ordering': ['order'], 'verbose_name': 'Отчет о расходах', 'verbose_name_plural': 'Отчеты о расходах'},
        ),
        migrations.AlterModelOptions(
            name='shelter',
            options={'ordering': ['order'], 'verbose_name': 'Приют', 'verbose_name_plural': 'Приюты'},
        ),
        migrations.AlterModelOptions(
            name='shelterphoto',
            options={'ordering': ['order'], 'verbose_name': 'Фотография приюта', 'verbose_name_plural': 'Фотографии приютов'},
        ),
        migrations.AddField(
            model_name='animal',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='animalphoto',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='moneyreport',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shelter',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shelterphoto',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
