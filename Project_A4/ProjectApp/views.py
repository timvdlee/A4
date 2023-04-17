from django.shortcuts import render


# Create your views here.


def home(request):
    return render(request, 'home.html')


def project_pagina(request):
    return render(request, 'project-pagina.html')


def project_toevoegen(request):
    return render(request, 'project-toevoegen.html',
                  {'title': 'Project toevoegen'})
