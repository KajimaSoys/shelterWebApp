from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import math
from django.utils import timezone


class OrderedModel(models.Model):
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        abstract = True


class Shelter(OrderedModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    name = models.CharField(max_length=255, verbose_name='Название')
    description = RichTextField(blank=True, verbose_name='Описание')
    city = models.CharField(max_length=255, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house = models.CharField(max_length=255, blank=True, verbose_name='Дом')
    rating = models.FloatField(default=0, verbose_name='Рейтинг')
    published = models.BooleanField(default=False, verbose_name='Опубликовано')
    additional_info = RichTextField(blank=True, verbose_name='Дополнительная информация')
    website_link = models.URLField(blank=True, verbose_name='Сайт')
    instagram_link = models.URLField(blank=True, verbose_name='Instagram')
    telegram_link = models.URLField(blank=True, verbose_name='Telegram')
    vk_link = models.URLField(blank=True, verbose_name='ВКонтакте')
    phone_number = models.CharField(max_length=255, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    @property
    def rounded_rating(self):
        return math.ceil(self.rating)

    def efficiency_rating(self):
        left_animals = self.animals.filter(status__in=['adopted', 'missing'])

        if not left_animals.exists():
            return 0

        total_stay_duration = sum(
            (animal.left_at - animal.created_at).total_seconds()
            for animal in left_animals
        )
        average_stay_duration = total_stay_duration / left_animals.count()
        average_stay_duration_days = average_stay_duration / (60 * 60 * 24)
        return average_stay_duration_days

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Приют'
        verbose_name_plural = 'Приюты'
        ordering = ['order']


class Animal(OrderedModel):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='animals', verbose_name='Приют')
    name = models.CharField(max_length=255, verbose_name='Имя')
    animal_type = models.CharField(max_length=255, verbose_name='Тип животного')
    breed = models.CharField(max_length=255, blank=True, verbose_name='Порода')
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='Возраст (месяцы)')

    gender_choices = (
        ('male', 'Самец'),
        ('female', 'Самка'),
        ('unknown', 'Неизвестно'),
    )
    gender = models.CharField(max_length=255, blank=True, verbose_name='Пол', choices=gender_choices)
    weight = models.IntegerField(null=True, blank=True, verbose_name='Вес (граммы)')
    health_status = models.TextField(blank=True, verbose_name='Состояние здоровья')
    description = RichTextField(blank=True, verbose_name='Описание')

    status_choices = (
        ('in_shelter', 'В приюте'),
        ('adopted', 'Приютили'),
        ('missing', 'Отсутствует'),
    )

    status = models.CharField(max_length=255, choices=status_choices, default='in_shelter', verbose_name='Статус животного')
    created_at = models.DateField(null=True, blank=True, verbose_name='Начало пребывания в приюте')
    left_at = models.DateField(null=True, blank=True, verbose_name='Окончание пребывания в приюте')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.status in ['adopted', 'missing'] and self.left_at is None:
            self.left_at = timezone.now().date()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Животное'
        verbose_name_plural = 'Животные'
        ordering = ['order']


class ShelterPhoto(OrderedModel):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='photos', verbose_name='Приют')
    photo = models.ImageField(upload_to='shelter_photos/', verbose_name='Фото')

    def __str__(self):
        return f'{self.shelter.name} - Фото {self.pk}'

    class Meta:
        verbose_name = 'Фотография приюта'
        verbose_name_plural = 'Фотографии приютов'
        ordering = ['order']


class AnimalPhoto(OrderedModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='photos', verbose_name='Животное')
    photo = models.ImageField(upload_to='animal_photos/', verbose_name='Фото')

    def __str__(self):
        return f'{self.animal.name} - Фото {self.pk}'

    class Meta:
        verbose_name = 'Фотография животного'
        verbose_name_plural = 'Фотографии животных'
        ordering = ['order']


class MoneyReport(OrderedModel):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='money_reports', verbose_name='Приют')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Потраченная сумма')
    photo = models.ImageField(upload_to='money_reports/', blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Отчет о расходах'
        verbose_name_plural = 'Отчеты о расходах'
        ordering = ['order']
