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
                'placeholder': 'Enter the title',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter the description',
                'rows': 4,
            }),
            'priority': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={
                'class': 'form-select',
            }),
            'deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) > 128:
            self.add_error('title', 'Title is too long')
        return title

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline <= timezone.now():
            self.add_error('deadline', 'Deadline must be equal current date or less')
        return deadline

    def clean_priority(self):
        priority = self.cleaned_data.get("priority")
        if priority < 1 or priority > 5:
            self.add_error('priority', 'Priority must be from 1 to 5')
        return priority
