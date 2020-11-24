from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ('email', 'username', 'password1', 'password2'):
            self.fields[field_name].help_text = ''


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']
