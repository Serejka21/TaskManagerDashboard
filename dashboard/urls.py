from django.urls import path

from .views import (index,
                    ProjectListView,
                    user_task_list, )


urlpatterns = [
    path("", index, name="index"),
    path("projects/",
         ProjectListView.as_view(),
         name="projects"),
    path("<int:pk>/my-tasks/", user_task_list, name="my-tasks")
    ]

app_name = "dashboard"
