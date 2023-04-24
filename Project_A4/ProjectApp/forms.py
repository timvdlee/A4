from ProjectApp.models import Project, Todo
from django import forms

class ProjectNaam(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(),
        required=True
    )

    class Meta:
        model = Project
        fields = ['name']



class TodoForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(),
        required=True
    )
    deadline_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    deadline_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True
    )
    completed = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False
    )

    class Meta:
        model = Todo
        fields = [
            'project',
            'name',
            'deadline_date',
            'deadline_time',
            'completed',
        ]
from django import forms
from .models import Project


class ProjectFrom(forms.ModelForm):
    naam = forms.CharField(required=False)

    class Meta:
        model = Project
        fields = ["Naam_project", "Admin", "Datum_aangemaakt"]
