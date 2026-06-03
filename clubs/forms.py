from django import forms
from .models import Club


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }
