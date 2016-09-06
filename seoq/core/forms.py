from django import forms

# our new form
class UserContactForm(forms.Form):
    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name',required=True)
    location = forms.CharField(label='Location',required=True)
    phone = forms.CharField(label='Phone',required=True)
    email = forms.EmailField(label='Email',required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super(UserContactForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
           field = self.fields.get(field_name)  
           if field:
               field.widget.attrs.update({
               		'placeholder': field.label,
               		'class': 'form-control'
               	})
        self.fields['content'].widget.attrs.update({
    		'placeholder': 'What do you want to say?',
    		'rows': 5
    	})
