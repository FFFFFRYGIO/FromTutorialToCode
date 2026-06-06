"""Django forms — declarative form handling and validation."""

from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "What needs doing?", "autofocus": True}
            ),
        }
