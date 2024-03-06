from django.urls import path

from .views import (index,
                    ProjectListView,
                    user_task_list,
                    ProjectDetailView, )


urlpatterns = [
    path("", index, name="index"),
    path("projects/",
         ProjectListView.as_view(),
         name="projects"),
    path("projects/<int:pk>/",
         ProjectDetailView.as_view(),
         name="project-detail"),
    path("my-tasks/<str:username>/", user_task_list, name="my-tasks")
    ]

app_name = "dashboard"
