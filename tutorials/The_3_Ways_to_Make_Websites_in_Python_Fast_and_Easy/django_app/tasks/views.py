"""Views — mixing a class-based view with simple function views."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from .forms import TaskForm
from .models import Task


class TaskListView(ListView):
    """Display all tasks and an "add task" form on the same page."""

    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm()
        context["remaining"] = Task.objects.filter(done=False).count()
        return context


def add_task(request):
    """Handle the create-task form POST."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f"Added task: {task.title}")
        else:
            messages.error(request, "Please fix the errors in the form.")
    return redirect("task_list")


def toggle_task(request, pk: int):
    """Flip a task's done status."""
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save(update_fields=["done"])
    return redirect("task_list")


def delete_task(request, pk: int):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, "Task deleted.")
    return redirect("task_list")
