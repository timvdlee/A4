from django.shortcuts import render
from .forms import ProjectNaam, TodoForm, ProjectFrom
# Create your views here.


def home(request):
    return render(request, 'home.html')


def project_pagina(request):
    todos = [
        {
            "name": "Maken van loginpagina + register page",
            "deadline": "20-04-2013 16:17",
            "subtodos": [{"description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis at felis vitae nunc euismod molestie non et ligula. Nullam tempus, tortor eu fringilla maximus, nibh augue vehicula erat, at condimentum sapien lorem non sem. Sed fermentum hendrerit pretium. Nullam faucibus risus ac elit interdum, vel rutrum turpis rhoncus. Curabitur eget nibh in arcu auctor gravida. Phasellus porta ante non dolor scelerisque porttitor. Integer at egestas tortor. Vivamus pellentesque vehicula sagittis."} for _ in range(10)]
        } for _ in range(10)
    ]
    
    finished_todos = [{"name":"Maken van een maken van een weet ik wel abcdefghijklmnopqrstuvwxyz","id":5} for _ in range(50)]
    project_name = ProjectNaam()
    todoform = TodoForm()
    
    project_users = [
        {"username":"Hoi","role":"Gebruiker","img":"none"}
        for _ in range(6)
    ]
    return render(request, 'project.html',
                  {
                      "todos":todos,
                      "finished_todos":finished_todos,
                      "project_name": project_name,
                      "todoform": todoform,
                      "project_users": project_users
                   }
                  )


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
