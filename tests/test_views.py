from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from dashboard.models import Position, Worker, TaskType, Project, Task


class DashboardViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.position = Position.objects.create(name="Test Position")
        self.worker = Worker.objects.create(
            username="workeruser", password="workerpass", position=self.position
        )
        self.task_type = TaskType.objects.create(type="Test Type")
        self.project = Project.objects.create(
            project_name="Test Project",
            description="Test Description",
            is_completed=False,
        )
        self.project.assignees.add(self.user)
        self.task = Task.objects.create(
            task_name="Test Task",
            description="Test Description",
            deadline="2022-12-31",
            is_completed=False,
            priority="medium",
            task_type=self.task_type,
            project=self.project,
        )
        self.task.assignees.add(self.user, self.worker)

    def test_index_view(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)

    def test_project_list_view(self):
        response = self.client.get(reverse("dashboard:projects"))
        self.assertEqual(response.status_code, 200)

    def test_update_task_view(self):
        test_task_name = "Task"
        response = self.client.post(
            reverse("dashboard:task-edit", kwargs={"pk": self.task.id}),
            data={"task_name": test_task_name},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_project_view(self):
        test_project_name = "Project"
        response = self.client.post(
            reverse("dashboard:project-edit", kwargs={"pk": self.project.id}),
            data={"project_name": test_project_name},
        )
        self.assertEqual(response.status_code, 302)
