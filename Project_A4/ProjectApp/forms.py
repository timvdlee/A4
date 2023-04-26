from django import forms
from .models import Project
from django.contrib.auth import get_user_model


class ProjectForm(forms.ModelForm):
    name = forms.CharField(required=False)
    # members = forms.ModelMultipleChoiceField(
    #     queryset=get_user_model().objects.filter(is_staff=False),
    #     widget=forms.SelectMultiple(attrs={'size': 10}),
    #     # Use SelectMultiple widget with 'size' attribute for scrollable list
    #     required=False
    # )
    deadline_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Project
        fields = ["name", "deadline_date"]
