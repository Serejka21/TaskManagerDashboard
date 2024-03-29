# Generated by Django 5.0.3 on 2024-03-06 21:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0004_project"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="task_list",
        ),
        migrations.AddField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="task",
                to="dashboard.project",
            ),
        ),
    ]
