from django import forms
from django.forms import widgets


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=widgets.PasswordInput)
