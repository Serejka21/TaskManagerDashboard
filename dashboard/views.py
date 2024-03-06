from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from dashboard.forms import TaskForm
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
    paginate_by = 5
    ordering = ["-created_at"]


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


def task_edit_view(request: HttpRequest, pk: int) -> HttpResponse:
    current_task = Task.objects.get(pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=current_task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("dashboard:task-detail",
                                                kwargs={"pk": current_task.id}))
    else:
        form = TaskForm(instance=current_task)
    return render(request, "dashboard/task_update_form.html", context={"form": form,
                                                             "current_task": current_task})


def task_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {
            "form": TaskForm()
        }
        return render(request, "dashboard/task_form.html", context=context)
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = Task.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse("dashboard:task-detail",
                                                kwargs={"pk": task.id}))
        context = {
            "form": form
        }

        return render(request, "dashboard/task_form.html", context=context)


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
