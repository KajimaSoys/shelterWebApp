from django.db import models


class Shelter(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house = models.CharField(max_length=255, blank=True)
    rating = models.FloatField()
    additional_info = models.TextField(blank=True)
    website_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    telegram_link = models.URLField(blank=True)
    vk_link = models.URLField(blank=True)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()
    money_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Animal(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='animals')
    animal_type = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    weight = models.FloatField(null=True, blank=True)
    health_status = models.TextField(blank=True)
    additional_info = models.TextField(blank=True)
    status = models.CharField(max_length=255)


class AnimalPhoto(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='photos')
    location_path = models.CharField(max_length=255)


class ShelterPhoto(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='photos')
    location_path = models.CharField(max_length=255)


class MoneyReport(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='money_reports')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    