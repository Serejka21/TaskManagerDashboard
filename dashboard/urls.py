from django.urls import path

from .views import (index,
                    ProjectListView,
                    user_task_list,
                    ProjectDetailView,
                    TaskDetailView,
                    task_edit_view,
                    task_create_view,
                    TaskListView,
                    project_create_view,
                    project_edit_view,
                    TaskListArchiveView, )


urlpatterns = [
    path("", index, name="index"),
    path("projects/",
         ProjectListView.as_view(),
         name="projects"),
    path("projects/<int:pk>/",
         ProjectDetailView.as_view(),
         name="project-detail"),
    path("projects/create/",
         project_create_view,
         name="project-create"),
    path("projects/<int:pk>/edit/",
         project_edit_view,
         name="project-edit"),
    path("task/list/",
         TaskListView.as_view(),
         name="task-list"),
    path("task/list/archive/",
         TaskListArchiveView.as_view(),
         name="task-list-archive"),
    path("task/create/",
         task_create_view,
         name="task-create"),
    path("task/<int:pk>/",
         TaskDetailView.as_view(),
         name="task-detail"),
    path("task/<int:pk>/edit/",
         task_edit_view,
         name="task-edit"),
    path("my-tasks/<str:username>/", user_task_list, name="my-tasks")
    ]

app_name = "dashboard"
