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
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'role', 'password1', 'password2']