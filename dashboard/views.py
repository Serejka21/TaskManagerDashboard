from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from dashboard.models import Task, TaskType


def index(request):
    num_tasks = Task.objects.count()
    last_added_task = Task.objects.all()
    context = {"num_tasks": num_tasks,
               "last_added_task": last_added_task}
    return render(request, "dashboard/index.html", context=context)


class TaskCategoryListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    queryset = TaskType.objects.select_related("task")
    template_name = "dashboard/task_category_list.html"
