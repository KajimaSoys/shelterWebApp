from django.contrib import admin
from .models import Shelter, Animal, AnimalPhoto, ShelterPhoto, MoneyReport
from .forms import AnimalPhotoForm, ShelterPhotoForm
import nested_admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin


class ShelterPhotoInline(nested_admin.NestedStackedInline):
    model = ShelterPhoto
    form = ShelterPhotoForm
    extra = 0


class MoneyReportInline(nested_admin.NestedStackedInline):
    model = MoneyReport
    extra = 1


class AnimalPhotoInline(nested_admin.NestedStackedInline):
    model = AnimalPhoto
    form = AnimalPhotoForm
    extra = 0


class AnimalInline(nested_admin.NestedStackedInline):
    model = Animal
    extra = 1
    inlines = [AnimalPhotoInline]


class ShelterAdmin(SortableAdminMixin, nested_admin.NestedModelAdmin):
    list_display = ('name', 'city', 'email', 'phone_number', 'published', 'rating')
    list_filter = ('published', 'city', 'rating')
    search_fields = ('name', 'city', 'email', 'phone_number')
    readonly_fields = ('rating', 'owner')
    inlines = [ShelterPhotoInline, MoneyReportInline, AnimalInline]

    def save_model(self, request, obj, form, change):
        """
        When creating a new object, set the author field.
        """
        if not change:
            obj.owner = request.user
        obj.save()


class AnimalAdmin(SortableAdminMixin, nested_admin.NestedModelAdmin):
    list_display = ('name', 'shelter', 'animal_type', 'breed', 'age', 'gender', 'status')
    list_filter = ('shelter', 'animal_type', 'breed', 'gender')
    search_fields = ('name', 'animal_type', 'breed')
    inlines = [AnimalPhotoInline]


class AnimalPhotoAdmin(SortableAdminMixin, nested_admin.NestedModelAdmin):
    list_display = ('animal', 'photo_preview', 'photo')
    list_filter = ('animal',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain;"/>', obj.photo.url)
        return "Изображение отсутствует"

    photo_preview.short_description = "Превью"


class ShelterPhotoAdmin(SortableAdminMixin, nested_admin.NestedModelAdmin):
    list_display = ('shelter', 'photo_preview', 'photo')
    list_filter = ('shelter',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: contain;" />', obj.photo.url)
        return "Изображение отсутствует"

    photo_preview.short_description = "Превью"


class MoneyReportAdmin(SortableAdminMixin, nested_admin.NestedModelAdmin):
    list_display = ('shelter', 'title', 'amount_spent', 'photo')
    list_filter = ('shelter',)
    search_fields = ('title',)


admin.site.register(Shelter, ShelterAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(AnimalPhoto, AnimalPhotoAdmin)
admin.site.register(ShelterPhoto, ShelterPhotoAdmin)
admin.site.register(MoneyReport, MoneyReportAdmin)
