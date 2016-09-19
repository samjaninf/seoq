from django import forms
from .models import User
from .widgets import ArraySelect, ArrayWidget


class EditProfileForm(forms.ModelForm):
    #profile_picture = forms.ImageField(
    #    required=False)

    areas_of_expertise = ArraySelect(forms.CharField(max_length=50), widget=ArrayWidget(choices=User.EXPERTISE_CHOICES),required=False)
    areas_of_expertise_other = forms.CharField(max_length=50, required=False, label='Other areas of expertise')
    languages = ArraySelect(forms.CharField(max_length=50), widget=ArrayWidget(choices=User.LANGUAGE_CHOICES),required=False)
    title = forms.CharField( required=False, 
      widget=forms.TextInput(attrs={'placeholder': 'e.g. SEO Professional and Marketing Consultant'}))
    about = forms.CharField(required=False,label='Your Bio', widget=forms.Textarea)
    location = forms.CharField(required=False,label='Current Location')
    languages_other = forms.CharField(required=False,label='Other Languages',max_length=50)
    fb_account = forms.URLField(required=False, max_length=255,label='Facebook Page')
    twitter_account = forms.URLField(required=False, max_length=255,label='Twitter Page')
    linkedin_account = forms.URLField(required=False, max_length=255,label='Linkedin Page')
    google_account = forms.URLField(required=False, max_length=255,label='Google+ Page')
    skype = forms.CharField(max_length=50, required=False, label='Skype username')

    class Meta:
        model = User
        fields = ["first_name", "last_name", 'fb_account',
                  'twitter_account', 'linkedin_account',
                  'google_account', 'skype', 'location', 'phone_number',
                  'title', 'about', 'profile_picture',
                  'website_url',
                  'areas_of_expertise', 'areas_of_expertise_other',
                  'languages', 'languages_other', 'company_name',
                  'company_logo']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['fb_account'].widget.attrs.update({
          'placeholder': 'https://www.facebook.com/SEOQuotient'})
        self.fields['twitter_account'].widget.attrs.update({
          'placeholder': 'https://twitter.com/SEOQuotient'})
        self.fields['linkedin_account'].widget.attrs.update({
          'placeholder': 'https://www.linkedin.com/in/SEOQuotient'})
        self.fields['google_account'].widget.attrs.update({
          'placeholder': 'https://plus.google.com/SEOQuotient'})
