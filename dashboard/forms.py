from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q

from dashboard.models import Task, Project


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"})
        }

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
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"})
        }

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False)

    def clean_is_completed(self):
        is_completed = self.cleaned_data["is_completed"]
        project = self.cleaned_data.get("id")
        if is_completed and Task.objects.filter(Q(project=project) | Q(is_completed=False)):
            raise ValidationError("You cant complete this project, "
                                  "because you have not completed tasks")
        return is_completed
