from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from dashboard.models import Task, TaskType, Worker, Project


def index(request):
    num_tasks = Task.objects.count()
    last_added_task = Task.objects.latest("created_at")
    context = {"num_tasks": num_tasks,
               "last_added_task": last_added_task}
    return render(request, "dashboard/index.html", context=context)


class ProjectListView(generic.ListView):
    model = Project
    queryset = Project.objects.filter(is_completed=False)

    class Meta:
        ordering = ['-created_at']


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()


@login_required
def user_task_list(request: HttpRequest, username: str) -> HttpResponse:
    current_user = get_user_model().objects.get(username=username)
    tasks = current_user.task.all()
    context = {"tasks": tasks}
    if request.method == "GET":
        return render(request,
                      "dashboard/user_task_list.html",
                      context=context)


