import django_filters
from .models import Shelter
from django.db.models import Max, Min


class ShelterFilter(django_filters.FilterSet):
    city = django_filters.ChoiceFilter(choices=[])
    rating = django_filters.RangeFilter()

    class Meta:
        model = Shelter
        fields = ['city', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['city'].extra.update({
            'choices': [(city, city) for city in Shelter.objects.values_list('city', flat=True).distinct()]
        })
