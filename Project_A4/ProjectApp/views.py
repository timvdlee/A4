from django.shortcuts import render
from .forms import ProjectFrom


# Create your views here.


def home(request):
    return render(request, 'home.html')


def project_pagina(request):
    return render(request, 'project-pagina.html')


def project_toevoegen(request):
    project_toev_form = ProjectFrom()
    if request.method == "POST":
        project_form_output = request.POST
        form = ProjectFrom(project_form_output)
        if form.is_valid():
            form.save()
    return render(request, 'project-toevoegen.html',
                  {'title': 'Project toevoegen',
                   'project_form': project_toev_form})
