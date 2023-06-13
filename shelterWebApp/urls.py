"""
URL configuration for shelterWebApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from core import views

router = DefaultRouter()
router.register(r'animals', views.AnimalViewSet, basename='animal')
router.register(r'animal_photos', views.AnimalPhotoViewSet, basename='animal_photo')
router.register(r'shelter_photos', views.ShelterPhotoViewSet, basename='shelter_photo')
router.register(r'money_reports', views.MoneyReportViewSet, basename='money_report')

urlpatterns = [
    re_path(r'^_nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),

    path('api/v1/', include(router.urls)),
    path('api/v1/register/', views.RegisterView.as_view(), name='register'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/user-details/', views.UserDetailsView.as_view(), name='user-details'),

    path('api/v1/shelters/', views.ShelterListCreateView.as_view(), name='shelter-list-create'),
    path('api/v1/shelters/<int:pk>/', views.ShelterRetrieveUpdateDestroyView.as_view(), name='shelter-retrieve-update-destroy'),
    path('api/v1/shelters/cities/', views.unique_cities, name='unique-cities'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
