from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    comment = forms.CharField(label=False,required=True,widget=forms.Textarea(attrs={'rows':3,'placeholder':'Add your comments...'}))
    
    class Meta:
        model = Comment
        fields = ['comment']
        
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if len(comment) < 10:
            raise forms.ValidationError("Comments must be atleast 10 characters long")
        return comment