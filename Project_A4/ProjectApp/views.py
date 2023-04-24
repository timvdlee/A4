from django.shortcuts import render

# Create your views here.




def home(request):
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
    return render(request, 'project-toevoegen.html')



