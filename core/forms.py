from django import forms
from django.utils.html import format_html
from .models import AnimalPhoto, ShelterPhoto


class AnimalPhotoForm(forms.ModelForm):
    class Meta:
        model = AnimalPhoto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.photo:
            self.fields['photo'].help_text = format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px; object-fit: contain;" />',
                self.instance.photo.url
            )


class ShelterPhotoForm(forms.ModelForm):
    class Meta:
        model = ShelterPhoto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.photo:
            self.fields['photo'].help_text = format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px; object-fit: contain;" />',
                self.instance.photo.url
            )
