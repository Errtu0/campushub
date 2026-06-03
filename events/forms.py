from django import forms
from .models import Event
from clubs.models import Club


class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'max_participants', 'club']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'club': forms.Select(attrs={'class': 'form-select'}),
        }

    # Filters the club dropdown based on who is filling the form.
    # Managers only see their own approved clubs; admins see all approved clubs.
    # user is keyword-only to avoid conflicts with ModelForm's positional args.
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_club_manager():
            self.fields['club'].queryset = Club.objects.filter(manager=user, status='approved')
        elif user and user.is_admin():
            self.fields['club'].queryset = Club.objects.filter(status='approved')
        else:
            self.fields['club'].queryset = Club.objects.none()
