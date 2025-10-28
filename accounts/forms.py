from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from tempus_dominus.widgets import DatePicker

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateTimeField(
        label=False,
        required=True,
        widget=DatePicker(
            attrs = {
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    class Meta:
        model = Profile
        fields = ['profile_picture','education','skills','job_title','phone','bio','location','date_of_birth']
