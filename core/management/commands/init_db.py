from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from core.models import Animal, Shelter
import csv
import os


class Command(BaseCommand):
    help = 'Initialize database'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@test.ru', '12345')
            self.stdout.write(self.style.SUCCESS('Admin user has been created'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user already exist'))

        if not Animal.objects.exists():
            script_dir = os.path.dirname(__file__)
            rel_path = "init_data/requester_animal.sql"
            abs_file_path = os.path.join(script_dir, rel_path)
            with open(abs_file_path, 'r') as f:
                with connection.cursor() as cursor:
                    cursor.execute(f.read())
            self.stdout.write(self.style.SUCCESS('Animals data has been inserted'))
        else:
            self.stdout.write(self.style.SUCCESS('Animals data already exist'))


        if not Shelter.objects.exists():
            script_dir = os.path.dirname(__file__)
            rel_path = "init_data/requester_shelter.sql"
            abs_file_path = os.path.join(script_dir, rel_path)
            with open(abs_file_path, 'r') as f:
                with connection.cursor() as cursor:
                    cursor.execute(f.read())
            self.stdout.write(self.style.SUCCESS('Shelters data has been inserted'))
        else:
            self.stdout.write(self.style.SUCCESS('Shelters data already exist'))