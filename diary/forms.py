from django import forms
from .models import DiaryEntry

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'markdownx-editor'}),
        }