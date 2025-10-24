from django import forms
from tempus_dominus.widgets import DatePicker
from .models import *
from project_app.utils import *
from django.contrib.auth.models import User

class TaskUpdateForm(forms.ModelForm):
    task_id = forms.IntegerField(widget=forms.HiddenInput(),required=True)
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':3,'placeholder':'Write description'}
        ),
        required=False
    )
    start_date = forms.DateTimeField(
        
        widget=DatePicker(
            attrs={'append':'fa fa-calendar','icon_toggle':True}
        )
    )
    due_date = forms.DateTimeField(
        
        widget=DatePicker(
            attrs={'append':'fa fa-calendar','icon_toggle':True}
        )
    )
    priority = forms.ChoiceField(
        
        choices=PRIORITY_CHOICES,
        widget=forms.Select(
            attrs={'class':'form-control'}
        ),
        required=True
    )
    class Meta:
        model = Task
        fields = ['name','description','priority','start_date','due_date']
        
class TaskAssignForm(forms.ModelForm):
    task_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    task_assigned_to = forms.ModelChoiceField(
        label=False,
        required=True,
        queryset= User.objects.none(),
        empty_label = 'Select User',
        widget=forms.Select(
            attrs={'class':'form-control'}
        )
    )
    class Meta:
        model = Task
        fields = ['task_id','task_assigned_to']
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        task_id = self.initial.get('task_id') or self.data.get('task_id')
        if task_id:
            try:
                task = Task.objects.get(id=task_id)
                self.fields['task_assigned_to'].queryset = task.project.team.members.all()
            except Task.DoesNotExist:
                self.fields['task_assigned_to'].queryset = User.objects.none()

