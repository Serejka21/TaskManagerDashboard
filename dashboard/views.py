from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from dashboard.forms import TaskForm, ProjectForm
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


class ProjectArchiveListView(generic.ListView):
    model = Project
    queryset = Project.objects.filter(is_completed=True)
    paginate_by = 5
    ordering = ["-created_at"]
    template_name = "dashboard/project_list_archive.html"


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 6
    ordering = ["-created_at"]


class TaskListArchiveView(generic.ListView):
    model = Task
    paginate_by = 6
    ordering = ["-created_at"]
    template_name = "dashboard/task_list_archive.html"


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


@transaction.atomic
def task_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {
            "form": TaskForm()
        }
        return render(request, "dashboard/task_form.html", context=context)
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            data = {
                "task_name": form.cleaned_data["task_name"],
                "description": form.cleaned_data["description"],
                "deadline": form.cleaned_data["deadline"],
                "is_completed": form.cleaned_data["is_completed"],
                "priority": form.cleaned_data["priority"],
                "task_type": form.cleaned_data["task_type"],
            }
            task = Task.objects.create(**data)
            task.assignees.set(form.cleaned_data["assignees"])
            task.project.set(form.cleaned_data["project"])
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


@login_required
def project_edit_view(request: HttpRequest, pk: int) -> HttpResponse:
    current_project = Project.objects.get(pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=current_project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("dashboard:project-detail",
                                                kwargs={"pk": current_project.id}))
    else:
        form = ProjectForm(instance=current_project)
    return render(request,
                  "dashboard/project_update_form.html",
                  context={"form": form,
                           "current_project": current_project})


@login_required
@transaction.atomic
def project_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {
            "form": ProjectForm()
        }
        return render(request, "dashboard/project_form.html", context=context)
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            data = {
                "project_name": form.cleaned_data["project_name"],
                "description": form.cleaned_data["description"],
                "is_completed": form.cleaned_data["is_completed"],
            }

            project = Project.objects.create(**data)
            project.assignees.set(form.cleaned_data["assignees"])
            return HttpResponseRedirect(reverse("dashboard:project-detail",
                                                kwargs={"pk": project.id}))
        context = {
            "form": form
        }

        return render(request, "dashboard/project_form.html", context=context)
