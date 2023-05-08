from ProjectApp.models import Project, Todo
from django import forms
from django.contrib.auth import get_user_model


class ProjectForm(forms.ModelForm):
    name = forms.CharField(required=True,max_length=Project._meta.get_field('name').max_length)
    deadline_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
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
            'name',
            'deadline_date',
            'deadline_time',
            'completed',
        ]