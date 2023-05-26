from ProjectApp.models import Project, Todo
from django import forms
from django.contrib.auth import get_user_model


class ProjectForm(forms.ModelForm):
    """ProjectForm
    
    Het form waarmee gebruikers de informatie over het project kunnen aanpassen. 
    Het enige wat aangepast kan worden is de naam. De deadline wordt automatisch door het script ingesteld. 
    De maximale lengte van het veld wordt bepaald door de maximum lengte uit de models op te halen.

    """
    name = forms.CharField(required=True,max_length=Project._meta.get_field('name').max_length)
    deadline_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Project
        fields = ['name', 'deadline_date']



class TodoForm(forms.ModelForm):
    """TodoForm
    De form waarmee de todo aangemaakt of aangepast kan worden. 
    Afhankelijk van wat de gebruiker wilt wordt deze form ingeladen met een bestaande todo. 

    :param forms: _description_
    """
    name = forms.CharField(
        max_length=Todo._meta.get_field('name').max_length,
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