from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .models import Shelter, Animal, AnimalPhoto, ShelterPhoto, MoneyReport
from .serializers import ShelterSerializer, AnimalSerializer, AnimalPhotoSerializer, ShelterPhotoSerializer, MoneyReportSerializer, RegisterSerializer


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
    serializer_class = ShelterSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class ShelterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    permission_classes = [IsShelterOwner | permissions.IsAdminUser]


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