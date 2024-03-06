from django import forms
from django.contrib.auth import get_user_model

from dashboard.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False)
