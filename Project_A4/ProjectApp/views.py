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
from .models import Todo,SubTodo
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
    
    if request.method == "POST":
        if 'project-name-submit' in request.POST: # project naam aanpassen
            project.name = request.POST.get("name")
            project.save()
        elif 'todo-toevoegen-submit' in request.POST: # Nieuwe todo aanmaken
            todo_form = TodoForm(request.POST)
            todo_form.completed = False
            if todo_form.is_valid():
                td_db_obj = todo_form.save(commit=False)
                td_db_obj.project = project
                td_db_obj.save()
        elif 'todo-update-submit' in request.POST: # Todo aanpassen
            todo = Todo.objects.get(id=request.POST.get("id"))
            todo.name = request.POST.get("name")
            todo.project = project
            todo.deadline_date = request.POST.get("deadline_date")
            todo.deadline_time = request.POST.get("deadline_time")
            todo.completed = True if request.POST.get("completed") else False
            todo.save()
        elif 'addSubTodo-submit' in request.POST: # Subtodo aanmaken
            subTodoDesc = request.POST.get("subTodoDesc")
            if len(subTodoDesc) > 0:
                subtodo = SubTodo()
                subtodo.todo = Todo.objects.get(id=request.POST.get("todoId"))
                subtodo.description = subTodoDesc
                subtodo.save()
        elif 'completeSubTodo-submit' in request.POST: # Subtodo verwijderen
            subtodo = SubTodo.objects.filter(id=request.POST.get("subTodoId"))
            if len(subtodo) > 0:
                subtodo[0].delete()
        elif 'reActivateTodo-submit' in request.POST: # Todo's activeren
            todo = Todo.objects.get(id=request.POST.get("id"))
            todo.completed = False
            todo.save()
            
    

    project_users = [{"username": user.username, "role": "Admin" if user == project.admin_user else "Gebruiker","img":"none"} for user in project.members.all()]

    
    start_date = datetime(2023, 4, 24)
    end_date = datetime(2023, 12, 31)


    
    todos = [
        {
        "name": todo.name,
        "deadline_date": todo.deadline_date,
        "deadline_time": todo.deadline_time,
        "id": todo.id,
        "completed": todo.completed,
        "subtodos": [{"description": subTodo.description,"id":subTodo.id}
         for subTodo in SubTodo.objects.filter(todo=todo)   
        ]
        }
        for todo in Todo.objects.filter(project=project, completed=False)
    ]
    todo_forms = [
        {
            'todo': todo,
            'form': TodoForm(initial={
                'name': todo['name'],
                'deadline_date': todo['deadline_date'],
                'deadline_time': todo['deadline_time'],
                'completed': todo['completed']
                })
            }
        for todo in todos
        ]

    finished_todos = [
        {
            "name": fin_todo.name,
            "id": fin_todo.id
            } for fin_todo in Todo.objects.filter(project=project, completed=True)
        ]
    project_name_form = ProjectForm(
        initial={
            'name': project.name
        }
    )
    
    add_todo = TodoForm()
    
 

    return render(request, 'project.html',
                  {
                      "project_obj": project,
                      "project_users": project_users,
                      "finished_todos": finished_todos,
                      "project_name_form": project_name_form,
                      "todo_form": todo_forms,
                      "todos": todos,
                      "project_naam": project.name,
                      "add_todo": add_todo,
                   }
                  )

@login_required
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