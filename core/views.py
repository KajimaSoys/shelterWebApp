# django
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import connection
import django_filters

# rest framework
from rest_framework import generics, permissions, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# project
from .models import Shelter, Animal, AnimalPhoto, ShelterPhoto, MoneyReport
from .serializers import ShelterSerializer, ShelterListSerializer, AnimalSerializer, AnimalPhotoSerializer, ShelterPhotoSerializer, MoneyReportSerializer, RegisterSerializer
from .filters import ShelterFilter


class StandardResultsSetPagination(PageNumberPagination):
    """Класс для пагинации результатов"""
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        })


class RegisterView(generics.CreateAPIView):
    """Вью для регистрации пользователя"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class IsShelterOwner(permissions.BasePermission):
    """Проверка является ли пользователь владельцем приюта"""
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Animal) or isinstance(obj, AnimalPhoto) or isinstance(obj, MoneyReport):
            return request.user == obj.shelter.user
        return request.user == obj.user


class ShelterListCreateView(generics.ListCreateAPIView):
    """Вью для получения и создания приютов"""
    queryset = Shelter.objects.all()
    serializer_class = ShelterListSerializer
    search_fields = ['name', 'city', 'email', 'phone_number']

    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ShelterFilter

    pagination_class = StandardResultsSetPagination
    ordering = ['order']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class ShelterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Вью для получения, обновления и удаления приютов"""
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    ordering = ['order']

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsShelterOwner(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShelterSerializer  # The detailed serializer
        return ShelterListSerializer  # The basic serializer


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def unique_cities(request):
    """Функция для получения уникальных городов"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT city FROM core_shelter")
        cities = [row[0] for row in cursor.fetchall()]
    return JsonResponse(sorted(cities), safe=False)


class AnimalViewSet(viewsets.ModelViewSet):
    """Вью для работы с моделью Animal"""
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get_queryset(self):
        queryset = Animal.objects.all()
        shelter = self.request.query_params.get('shelter', None)
        if shelter is not None:
            queryset = queryset.filter(shelter=shelter)
        return queryset.select_related('shelter')

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsShelterOwner()]
        return [permissions.AllowAny()]


class AnimalPhotoViewSet(viewsets.ModelViewSet):
    """Вью для работы с моделью AnimalPhoto"""
    queryset = AnimalPhoto.objects.all()
    serializer_class = AnimalPhotoSerializer

    def get_queryset(self):
        queryset = AnimalPhoto.objects.all()
        animal = self.request.query_params.get('animal', None)
        if animal is not None:
            queryset = queryset.filter(animal=animal)
        return queryset.select_related('animal')

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsShelterOwner()]
        return [permissions.AllowAny()]


class ShelterPhotoViewSet(viewsets.ModelViewSet):
    """Вью для работы с моделью ShelterPhoto"""
    queryset = ShelterPhoto.objects.all()
    serializer_class = ShelterPhotoSerializer

    def get_queryset(self):
        queryset = ShelterPhoto.objects.all()
        shelter = self.request.query_params.get('shelter', None)
        if shelter is not None:
            queryset = queryset.filter(shelter=shelter)
        return queryset.select_related('shelter')

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsShelterOwner()]
        return [permissions.AllowAny()]


class MoneyReportViewSet(viewsets.ModelViewSet):
    """Вью для работы с моделью MoneyReport"""
    queryset = MoneyReport.objects.all()
    serializer_class = MoneyReportSerializer

    def get_queryset(self):
        queryset = MoneyReport.objects.all()
        shelter = self.request.query_params.get('shelter', None)
        if shelter is not None:
            queryset = queryset.filter(shelter=shelter)
        return queryset.select_related('shelter')

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsShelterOwner()]
        return [permissions.AllowAny()]
