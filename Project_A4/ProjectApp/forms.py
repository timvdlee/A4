from django import forms
from .models import Project


class ProjectFrom(forms.ModelForm):
    naam = forms.CharField(required=False)

    class Meta:
        model = Project
        fields = ["name", "members", "deadline_date"]
