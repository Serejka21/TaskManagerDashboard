from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from dashboard.models import Task, TaskType


@login_required
def index(request):
    return render(request, "index.html")


class TaskCategoryListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    queryset = TaskType.objects.select_related("task")
    template_name = "dashboard/task_category_list.html"
