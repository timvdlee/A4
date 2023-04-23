from django.shortcuts import render
from .forms import ProjectNaam, TodoForm
import uuid
import random
from datetime import datetime, timedelta
# Create your views here.




def home(request):
    return render(request, 'home.html')

def random_deadline(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    random_time = random.randrange(24 * 3600)
    return start_date + timedelta(days=random_days, seconds=random_time)


def project_pagina(request):
    start_date = datetime(2023, 4, 24)
    end_date = datetime(2023, 12, 31)

    todos = [
        {
            "name": f"Todo {str(uuid.uuid4())}",
            "deadline": (deadline := random_deadline(start_date, end_date)).strftime("%d-%m-%Y %H:%M"),
            "deadline-date": deadline.strftime("%Y-%m-%d"),
            "deadline_time": deadline.strftime("%H:%M"),
            "id": _,
            "subtodos": [
                {
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
                }
                for _ in range(10)
            ],
        }
        for _ in range(36)
    ]
    todo_forms = [
        {
            'todo': todo,
            'form': TodoForm(initial={
                'name': todo['name'],
                'deadline_date': todo['deadline-date'],
                'deadline_time': todo['deadline_time'],
                })
            }
        for todo in todos
        ]

    project_name = "Project"
    
    finished_todos = [
        {
            "name": "Maken van een maken van een weet ik wel abcdefghijklmnopqrstuvwxyz",
            "id": 5
            } for _ in range(50)
        ]
    project_name_form = ProjectNaam(
        initial={
            'name': project_name
        }
    )
    
    add_todo = TodoForm()

    return render(request, 'project.html',
                  {
                      "todos": todos,
                      "finished_todos": finished_todos,
                      "project_name_form": project_name_form,
                      "todo_form": todo_forms,
                      "project_naam": project_name,
                      "add_todo": add_todo,
                   }
                  )


def project_toevoegen(request):
    return render(request, 'project-toevoegen.html')



