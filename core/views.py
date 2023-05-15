from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .models import Shelter, Animal, AnimalPhoto, ShelterPhoto, MoneyReport
from .serializers import ShelterSerializer, ShelterListSerializer, AnimalSerializer, AnimalPhotoSerializer, ShelterPhotoSerializer, MoneyReportSerializer, RegisterSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
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
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class IsShelterOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Animal) or isinstance(obj, AnimalPhoto) or isinstance(obj, MoneyReport):
            return request.user == obj.shelter.user
        return request.user == obj.user


class ShelterListCreateView(generics.ListCreateAPIView):
    queryset = Shelter.objects.all()
    ordering = ['order']
    serializer_class = ShelterListSerializer
    pagination_class = StandardResultsSetPagination


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class ShelterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
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


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def get_queryset(self):
        shelter = self.request.query_params.get('shelter', None)
        if shelter is not None:
            return Animal.objects.filter(shelter=shelter)
        return Animal.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsShelterOwner()]
        return [permissions.AllowAny()]


class AnimalPhotoViewSet(viewsets.ModelViewSet):
    queryset = AnimalPhoto.objects.all()
    serializer_class = AnimalPhotoSerializer

    def get_queryset(self):
        animal = self.request.query_params.get('animal', None)
        if animal is not None:
            return AnimalPhoto.objects.filter(animal=animal)
        return AnimalPhoto.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsShelterOwner()]
        return [permissions.AllowAny()]


class ShelterPhotoViewSet(viewsets.ModelViewSet):
    queryset = ShelterPhoto.objects.all()
    serializer_class = ShelterPhotoSerializer

    def get_queryset(self):
        shelter = self.request.query_params.get('shelter', None)
        if shelter is not None:
            return ShelterPhoto.objects.filter(shelter=shelter)
        return ShelterPhoto.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsShelterOwner()]
        return [permissions.AllowAny()]


class MoneyReportViewSet(viewsets.ModelViewSet):
    queryset = MoneyReport.objects.all()
    serializer_class = MoneyReportSerializer


    def get_queryset(self):
        shelter = self.request.query_params.get('shelter', None)
        if shelter is not None:
            return MoneyReport.objects.filter(shelter=shelter)
        return MoneyReport.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsShelterOwner()]
        return [permissions.AllowAny()]
