from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from TaskApp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the description',
                'rows': 4,
            }),
            'priority': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={
                'class': 'form-select',
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
        }

        error_messages = {
            'title': {
                'required': _('Title is required.'),
                'max_length': _('Title length is too long.'),
            },
            'description': {
                'max_length': _('Title length is too long.'),
            },
            'priority': {
                'invalid': _('Choose priority from 1 to 5.'),
            },
            'deadline': {
                'invalid': _('Invalid DateTime format.'),
            },
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline <= timezone.now():
            return forms.ValidationError(_("Invalid deadline"))
        return deadline

    def clean_priority(self):
        priority = self.cleaned_data.get("priority")
        if priority < 1 or priority > 5:
            return forms.ValidationError(_("Invalid priority"))
        return priority

