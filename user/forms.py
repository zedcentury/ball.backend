# forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'full_name', 'image')  # Include any additional fields here

    # Optionally, add custom validation or initial values here if needed


class CustomUserChangeForm(UserChangeForm):
    pass
    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'profile_image')  # Include any additional fields here

    # Optionally, add custom validation or initial values here if needed
