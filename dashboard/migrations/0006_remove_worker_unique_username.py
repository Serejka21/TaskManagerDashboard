# Generated by Django 5.0.3 on 2024-03-12 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0005_remove_project_task_list_task_project"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="worker",
            name="unique_username",
        ),
    ]
