from django import forms
from .models import User
from .widgets import ArraySelect, ArrayWidget


class EditProfileForm(forms.ModelForm):
    #profile_picture = forms.ImageField(
    #    required=False)

    areas_of_expertise = ArraySelect(forms.CharField(max_length=50), widget=ArrayWidget(choices=User.EXPERTISE_CHOICES))
    languages = ArraySelect(forms.CharField(max_length=50), widget=ArrayWidget(choices=User.LANGUAGE_CHOICES))

    class Meta:
        model = User
        fields = ["first_name", "last_name", 'fb_account',
                  'twitter_account', 'linkedin_account',
                  'title', 'about', 'profile_picture',
                  'website_url', 'website_url1', 'website_url2',
                  'website_url3', 'website_url4',
                  'areas_of_expertise', 'areas_of_expertise_other',
                  'languages', 'languages_other']
