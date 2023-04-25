from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from .forms import ProjectForm,TodoForm
from datetime import datetime
from .models import Project
from django.contrib.auth import get_user_model
import json
from django.contrib.auth.decorators import login_required
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


def project(request,pk=None):
    project = get_object_or_404(Project, pk=pk)
    
    project_name = project.name
    
    start_date = datetime(2023, 4, 24)
    end_date = datetime(2023, 12, 31)

    todos = [
        {
            "name": f"{str(uuid.uuid4())}",
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

    
    finished_todos = [
        {
            "name": "Maken van een maken van een weet ik wel abcdefghijklmnopqrstuvwxyz",
            "id": 5
            } for _ in range(50)
        ]
    project_name_form = ProjectForm(
        initial={
            'name': project_name
        }
    )
    
    add_todo = TodoForm()

    return render(request, 'project.html',
                  {
                      "project_obj": project,
                      "finished_todos": finished_todos,
                      "project_name_form": project_name_form,
                      "todo_form": todo_forms,
                      "project_naam": project_name,
                      "add_todo": add_todo,
                   }
                  )


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
            return HttpResponseRedirect(f"/project/{obj.id}/")
    
    selectable_users = {i["username"]: i["id"] for i in get_user_model().objects.filter(is_staff=False).exclude(id=request.user.id).values()}
    selectable_users = json.dumps(selectable_users)
    
    
    
    return render(request, 'project-toevoegen.html',
                  {'title': 'Project toevoegen',
                   'project_form': project_toev_form,
                   "selectable_users":selectable_users})