from django import forms
from app.models import CustomUser

class UserForm(forms.Form):
    email = forms.EmailField()

    password = forms.CharField(widget=forms.PasswordInput())
