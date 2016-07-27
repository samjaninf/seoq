from django import forms


class ExampleForm(forms.Form):
    url = forms.URLField(required=True, initial='http://')
