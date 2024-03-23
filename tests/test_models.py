from django.test import TestCase
from django.contrib.auth import get_user_model
from dashboard.models import Position, Worker, TaskType, Project, Task


class PositionModelTest(TestCase):
    def test_str_method(self):
        position = Position.objects.create(name="Test Position")
        self.assertEqual(str(position), "Test Position")


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.worker = get_user_model().objects.create_user(
            username="testuser", first_name="Bob", last_name="Marley",
            password="testpass", position=self.position
        )

    def test_str_method(self):
        self.assertEqual(str(self.worker), "Bob Marley, position: Test Position")

    def test_has_perm_project_edit(self):
        self.assertFalse(self.worker.has_perm_project_edit())


class TaskTypeModelTest(TestCase):
    def test_str_method(self):
        task_type = TaskType.objects.create(type="Test Type")
        self.assertEqual(str(task_type), "Test Type")


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.project = Project.objects.create(
            project_name="Test Project",
            description="Test Description",
            is_completed=False,
        )
        self.project.assignees.add(self.user)

    def test_str_method(self):
        self.assertEqual(str(self.project), "Test Project")


class TaskModelTest(TestCase):
    def setUp(self):
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

    def test_str_method(self):
        self.assertEqual(str(self.task), "Test Task")
