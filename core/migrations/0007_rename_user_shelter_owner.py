# Generated by Django 4.2 on 2023-06-11 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_animal_options_alter_animalphoto_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shelter',
            old_name='user',
            new_name='owner',
        ),
    ]
