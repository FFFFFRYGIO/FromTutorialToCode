"""Register models with Django's built-in admin site."""

from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "done", "created_at")
    list_filter = ("done", "priority")
    search_fields = ("title",)
    list_editable = ("done", "priority")
