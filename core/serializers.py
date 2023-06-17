from rest_framework import serializers
from .models import Shelter, Animal, AnimalPhoto, ShelterPhoto, MoneyReport
from django.contrib.auth.models import User

gender_choices = (
        ('male', 'Самец'),
        ('female', 'Самка'),
        ('unknown', 'Неизвестно'),
    )

status_choices = (
        ('in_shelter', 'В приюте'),
        ('adopted', 'Приютили'),
        ('missing', 'Отсутствует'),
    )


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class AnimalPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalPhoto
        fields = ('id',
                  'photo',
                  'animal',)


class ShelterPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelterPhoto
        fields = ('id',
                  'photo',
                  'shelter',)


class MoneyReportSerializer(serializers.ModelSerializer):
    shelter_owner = serializers.ReadOnlyField(source='shelter.owner.id')

    class Meta:
        model = MoneyReport
        fields = ('id',
                  'title',
                  'description',
                  'amount_spent',
                  'photo',
                  'shelter',
                  'shelter_owner',)


class AnimalSerializer(serializers.ModelSerializer):
    photos = AnimalPhotoSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=gender_choices)
    shelter_owner = serializers.ReadOnlyField(source='shelter.owner.id')
    shelter_name = serializers.ReadOnlyField(source='shelter.name')
    status = serializers.ChoiceField(choices=status_choices)
    # created_at = serializers.SerializerMethodField()
    # left_at = serializers.SerializerMethodField()
    #
    # def get_created_at(self, obj):
    #     return obj.created_at.date()
    #
    # def get_left_at(self, obj):
    #     return obj.left_at.date()

    class Meta:
        model = Animal
        fields = ('id',
                  'name',
                  'shelter',
                  'shelter_owner',
                  'shelter_name',
                  'animal_type',
                  'breed',
                  'age',
                  'gender',
                  'weight',
                  'health_status',
                  'description',
                  'status',
                  'created_at',
                  'left_at',
                  'photos')


class ShelterSerializer(serializers.ModelSerializer):
    animals = AnimalSerializer(many=True, read_only=True)
    photos = ShelterPhotoSerializer(many=True, read_only=True)
    money_reports = MoneyReportSerializer(many=True, read_only=True)
    efficiency_rating = serializers.SerializerMethodField()

    def get_efficiency_rating(self, obj):
        return obj.efficiency_rating()

    class Meta:
        model = Shelter
        fields = ('id',
                  'owner',
                  'name',
                  'description',
                  'city',
                  'street',
                  'house',
                  'rating',
                  'additional_info',
                  'website_link',
                  'instagram_link',
                  'telegram_link',
                  'vk_link',
                  'phone_number',
                  'email',
                  'efficiency_rating',
                  'animals',
                  'photos',
                  'money_reports')


class ShelterListSerializer(serializers.ModelSerializer):
    photos = ShelterPhotoSerializer(many=True, read_only=True)
    rounded_rating = serializers.IntegerField(read_only=True)
    efficiency_rating = serializers.SerializerMethodField()

    def get_efficiency_rating(self, obj):
        return obj.efficiency_rating()

    class Meta:
        model = Shelter
        fields = ('id',
                  'owner',
                  'name',
                  'city',
                  'street',
                  'house',
                  'additional_info',
                  'website_link',
                  'instagram_link',
                  'telegram_link',
                  'vk_link',
                  'phone_number',
                  'email',
                  'description',
                  'rating',
                  'rounded_rating',
                  'efficiency_rating',
                  'photos',
                  'order')
