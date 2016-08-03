from django import forms
from .models import User

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    profile_picture = forms.ImageField(
        required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", 
        		 'fb_account', 'twitter_account',
             	 'linkedin_account', 'title', 'about',
             	 'profile_picture']


