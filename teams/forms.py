from django import forms
from .models import *
from django.contrib.auth.models import User

class TeamForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'placeholder':'Describe Your Team Here...'}),required=True,label=False)
    
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Enter the name of your team here ..."}
        ),
        required=True,
        label=False
    )
    
    team_lead = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={'class':'form-control'}
        ),
        label=False,
        required=True
    )
    
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(
            attrs={'class':'form-control'}
        ),
        label=False,
        required=True
    )
    class Meta:
        model = Team
        fields = ['name','description','team_lead','members']