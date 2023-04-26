from django.shortcuts import render
from .forms import ProjectForm
from datetime import datetime
from .models import Project
from django.contrib.auth import get_user_model
import json


# Create your views here.


def home(request):
    print(Project.objects.all())
    projects = [
        {
            "name": f"Project {_+1}",
            "id": _ + 1,
            "date": "13-04-2023 14:00",
            "users": ["Jesse", "Ise", "Tim", "Salah"],
            "edit": "date"
        } for _ in range(10)
    ]
    return render(request, 'home.html',
                  {
                      "projects": projects,
                  })



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
            usr_list = json.loads(request.POST.get('members'))
            obj.members.add(request.user.id)
            for x in usr_list:
                obj.members.add(x)
            obj.save()
    
    selectable_users = {i["username"]: i["id"] for i in get_user_model().objects.filter(is_staff=False).exclude(id=request.user.id).values()}
    selectable_users = json.dumps(selectable_users)
    
    
    
    return render(request, 'project-toevoegen.html',
                  {'title': 'Project toevoegen',
                   'project_form': project_toev_form,
                   "selectable_users":selectable_users})
