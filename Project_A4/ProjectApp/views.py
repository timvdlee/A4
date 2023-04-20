from django.shortcuts import render
from .forms import ProjectForm
from datetime import datetime
from .models import Project


# Create your views here.


def home(request):
    return render(request, 'home.html')


def project_pagina(request):
    return render(request, 'project-pagina.html')


def project_toevoegen(request):
    project_toev_form = ProjectForm()
    if request.method == "POST":
        project_form_output = request.POST
        form = ProjectForm(project_form_output)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.admin_user = request.user
            obj.save()
            for x in (request.POST.getlist('members')):
                obj.members.add(x)
            obj.save()
    return render(request, 'project-toevoegen.html',
                  {'title': 'Project toevoegen',
                   'project_form': project_toev_form})
