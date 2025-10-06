from django import forms
from . models import Project
from teams.models import Team
from tempus_dominus.widgets import DatePicker
from .utils import *

class ProjectForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'placeholder':'Describe Your Projects Here...','id':'inputDescription','class':'form-control'}),required=True)
    start_date = forms.DateField(widget=DatePicker(attrs={'append':'fa fa-calendar','icon-toggle':True,'class':'form-control','id':'inputProjectLeader'}),required=True)
    client_company = forms.CharField(widget=forms.TextInput(attrs={'id':'inputClientCompany','class':'form-control'}),required=True)
    
    due_date = forms.DateTimeField(
        label=False,
        required=True,
        widget=DatePicker(
            attrs = {
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
    
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': "Enter the name of your project here ..."}
        ),
        required=True,
        label=False
    )
    
    
    
    team = forms.ModelChoiceField(
        queryset= Team.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
        label=False,
        required=True
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class':'form-control'}),
        label=False,
        required=True
    )
    
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class':'form-control'}),
        label=False,
        required=True
    )
    
    total_amount = forms.DecimalField(
        label=False,
        required=True
    )
    
    amount_spent = forms.DecimalField(
        label=False,
        required=True
    )
    
    estimated_duration = forms.DecimalField(
        label=False,
        required=True
    )
    
    class Meta:
        model = Project
        fields = ['name','team','description','client_company','priority','status','start_date','due_date','total_amount','amount_spent','estimated_duration']