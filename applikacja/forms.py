from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Catalog, Books


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = forms.ModelForm
        fields = ['username',
                  'password']


class CreateUserForm (UserCreationForm):
    class Meta:
        model = User
        fields = [  'username',
                    'first_name',
                    'last_name',
                    'email',
                    'password1',
                    'password2']


class RentalBookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['title',
                  'author']


