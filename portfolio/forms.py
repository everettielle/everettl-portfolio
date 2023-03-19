from django import forms
from django.contrib.auth.models import User
from .models import *


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        )


class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'open_profile',
            'birthday',
            'profile_photo',
        )
