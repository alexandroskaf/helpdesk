from django import forms
from django.contrib.auth.models import User
from .models import Room

class RoomForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)

    class Meta:
        model = Room
        fields = ['name', 'slug', 'users']  # Add users field
