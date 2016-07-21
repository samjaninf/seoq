from django import forms


class ExampleForm(forms.Form):
    keywords = forms.CharField(
        required=True,
        help_text='list of keywords separated by a comma')
    url = forms.URLField(required=True, initial='http://')
