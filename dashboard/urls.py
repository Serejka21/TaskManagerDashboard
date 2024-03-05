from django.urls import path

from .views import (index,
                    TaskCategoryListView, )


urlpatterns = [
    path("", index, name="index"),
    path("tasks-category/",
         TaskCategoryListView.as_view(),
         name="tasks-category")
    ]

app_name = "dashboard"
