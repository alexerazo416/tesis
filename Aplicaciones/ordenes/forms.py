from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
