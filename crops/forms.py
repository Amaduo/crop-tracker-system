from django import forms
from .models import Field, FieldUpdate
from django.contrib.auth.forms import UserCreationForm
from .models import User

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = '__all__'


class UpdateForm(forms.ModelForm):
    class Meta:
        model = FieldUpdate
        fields = ['stage', 'notes']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # REMOVE role field