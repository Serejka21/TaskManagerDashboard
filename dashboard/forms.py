from django import forms
from django.contrib.auth import get_user_model

from dashboard.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False)

    project = forms.ModelChoiceField(
        queryset=Project.objects.filter(is_completed=False),
        required=False
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False)
