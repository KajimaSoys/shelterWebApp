from rest_framework import serializers
from .models import Shelter, Animal, AnimalPhoto, ShelterPhoto, MoneyReport
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AnimalPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalPhoto
        fields = ('id',
                  'photo')


class ShelterPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelterPhoto
        fields = ('id',
                  'photo')


class MoneyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyReport
        fields = ('id',
                  'title',
                  'description',
                  'amount_spent',
                  'photo')


class AnimalSerializer(serializers.ModelSerializer):
    photos = AnimalPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Animal
        fields = ('id',
                  'name',
                  'shelter',
                  'animal_type',
                  'breed',
                  'age',
                  'gender',
                  'weight',
                  'health_status',
                  'description',
                  'photos')


class ShelterSerializer(serializers.ModelSerializer):
    animals = AnimalSerializer(many=True, read_only=True)
    photos = ShelterPhotoSerializer(many=True, read_only=True)
    money_reports = MoneyReportSerializer(many=True, read_only=True)

    class Meta:
        model = Shelter
        fields = ('id',
                  'user',
                  'name',
                  'description',
                  'city',
                  'street',
                  'house',
                  'rating',
                  'published',
                  'additional_info',
                  'website_link',
                  'instagram_link',
                  'telegram_link',
                  'vk_link',
                  'phone_number',
                  'email',
                  'animals',
                  'photos',
                  'money_reports')
