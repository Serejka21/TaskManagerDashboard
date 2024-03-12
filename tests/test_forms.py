from datetime import datetime

from django.test import TestCase

from dashboard import forms
from dashboard.forms import ProjectForm, TaskForm
from dashboard.models import TaskType, Task, Project


class ProjectTaskFormTest(TestCase):

    def setUp(self):
        self.task_type = TaskType.objects.create(type="test")
        self.project = Project.objects.create(project_name="test", description="test")

    def test_valid_project_form(self):
        form_data = {"project_name": "Test Project"}
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_project_form(self):
        form_data = {}
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["project_name"], ["This field is required."])

    def test_valid_task_form(self):
        form_data = {
            "task_name": "Test Task",
            "description": "Test Description",
            "priority": "High",
            "deadline": datetime.today(),
            "task_type": self.task_type,
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_project_with_task(self):
        task = Task.objects.create(
            task_name="Test",
            description="test",
            priority="high",
            deadline=datetime.today(),
            task_type=self.task_type,
            project=self.project,
        )
        form_data = {
            "name": "Test Project",
            "deadline": datetime.today(),
            "is_completed": True,
        }
        form = ProjectForm(data=form_data, instance=self.project)
        is_valid = form.is_valid()

        # Asserting that the form is not valid due to the expected validation error
        self.assertFalse(is_valid)
        self.assertIn("is_completed", form.errors)
        self.assertEqual(
            form.errors["is_completed"],
            ["You cant complete this project, because you have not completed tasks"],
        )
