from django import forms
from .models import *
from django.utils import timezone

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title','description','status','priority','due_date','tags')

    def clean_due_date(self):
        due=self.cleaned_data.get('due_date')
        status=self.cleaned_data.get('status') or self.instance.status
        if due and status != Task.Status.DONE and due < timezone.localdate():
            raise forms.ValidationError('Due date must be before today')
        return due
