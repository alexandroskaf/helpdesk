# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Room

class RoomForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # Start with an empty queryset
        widget=forms.CheckboxSelectMultiple,
        required=False  # Allow users to create a room without selecting other users
    )

    class Meta:
        model = Room
        fields = ['name', 'users']

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)  # Get the current user
        super(RoomForm, self).__init__(*args, **kwargs)
        if current_user:
            # Exclude the current user from the queryset
            self.fields['users'].queryset = User.objects.exclude(id=current_user.id)
