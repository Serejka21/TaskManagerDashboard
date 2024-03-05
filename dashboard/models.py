from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

from core import settings


class Position(models.Model):
    name = models.CharField(
        max_length=63,
    )

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position,
                                 on_delete=models.CASCADE,
                                 default=None,
                                 null=True,
                                 blank=True)

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"
        constraints = [UniqueConstraint(fields=["username"], name="unique_username")]
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}, " \
               f"position: {self.position}"


class TaskType(models.Model):
    type = models.CharField(
        max_length=63,
    )


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
        ("critical", "Critical"),
    ]

    task_name = models.CharField(
        max_length=63,
    )
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=63, choices=PRIORITY_CHOICES, default="medium"
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="task")
    assignees = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name="task")
