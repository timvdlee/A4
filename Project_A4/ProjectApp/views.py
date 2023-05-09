from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import ProjectForm, TodoForm
from datetime import datetime
from .models import Project, User, Recent
from django.contrib.auth import get_user_model
import json
from django.contrib.auth.decorators import login_required
from datetime import datetime 
from .models import Todo, SubTodo
from django.contrib import messages 

# Create your views here.

@login_required
def home(request):
    projects_with_user = Project.objects.filter(
        members=User.objects.get(id=request.user.id)).order_by('creation_date')
    recent_with_user = Recent.objects.filter(project__in=projects_with_user).order_by('-date', '-time')
    return render(request, 'home.html',
                  {
                      "projects": projects_with_user,
                      "feed": recent_with_user[:10],
                  })

def add_to_recent(project, user, description):
    date = datetime.now().date()
    time = datetime.now().time()
    add_recent = Recent(user=user, project=project, date=date, time=time,
                        description=description)
    add_recent.save()
    
def project_name_edit(request,project):
    add_to_recent(project, request.user, f"{request.user} heeft project {project.name} aangepast naar {request.POST.get('name')}")
    new_name = request.POST.get("name")
    if len(new_name) > 0 and len(new_name) <= Project._meta.get_field('name').max_length:
        project.name = new_name
        project.save()

def todo_toevoegen_submit(request,project):
    todo_form = TodoForm(request.POST)
    todo_form.completed = False
    if todo_form.is_valid():
        td_db_obj = todo_form.save(commit=False)
        td_db_obj.project = project
        td_db_obj.save()
        add_to_recent(project, request.user,
                        f"{request.user} heeft todo {td_db_obj.name} aangemaakt in project {project.name}")
        
def todo_update_submit(request,project):
    todo = Todo.objects.get(id=request.POST.get("id"))
    todo.name = request.POST.get("name")
    todo.project = project
    todo.deadline_date = request.POST.get("deadline_date")
    todo.deadline_time = request.POST.get("deadline_time")
    todo.completed = True if request.POST.get("completed") else False
    todo.save()
    add_to_recent(project, request.user, f"{request.user} heeft todo {todo.name} aangepast")
    
def addSubTodo_submit(request,project):
    subTodoDesc = request.POST.get("subTodoDesc")
    if len(subTodoDesc) > 0:
        subtodo = SubTodo()
        subtodo.todo = Todo.objects.get(id=request.POST.get("todoId"))
        subtodo.description = subTodoDesc
        subtodo.save()
        add_to_recent(project, request.user,
                        f"{request.user} heeft een subtodo aangemaakt in todo {subtodo.todo.name} van project {subtodo.todo.project.name}")

def completeSubTodo_submit(request,project):
    subtodo = SubTodo.objects.filter(id=request.POST.get("subTodoId"))
    if len(subtodo) > 0:
        add_to_recent(project, request.user,
                      f"{request.user} heeft een subtodo afgerond van todo {subtodo[0].todo.name} uit project {subtodo[0].todo.project.name}")
        subtodo[0].delete()
        
def reActivateTodo_submit(request,project):
    todo = Todo.objects.get(id=request.POST.get("id"))
    todo.completed = False
    todo.save()
    add_to_recent(project, request.user,
                    f"{request.user} heeft todo {todo.name} van project {todo.project.name} opnieuw geactiveerd")
    

def project_add_user(request,project):
    project = Project.objects.get(id=request.POST.get("project_id"))
    user = User.objects.filter(username=request.POST.get("users"))
    if len(user) > 0:
        user = user[0]
        project.members.add(user)
        project.save()
        add_to_recent(project, request.user,
                    f"{request.user} heeft {user} toegevoegd aan project {project.name}")
    else:
        messages.error(request,"User does not exist")

@login_required
def project(request, pk=None):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        match list(dict(request.POST).keys())[-1]:
            case 'project-name-submit':
                project_name_edit(request,project)
            case 'todo-toevoegen-submit':
                todo_toevoegen_submit(request,project)
            case 'todo-update-submit':
                todo_update_submit(request,project)
            case 'addSubTodo-submit':
                addSubTodo_submit(request,project)
            case 'completeSubTodo-submit':
                completeSubTodo_submit(request,project)
            case 'reActivateTodo-submit':
                reActivateTodo_submit(request,project)
            case 'project-add-user':
                project_add_user(request,project)

    project_users = [{"username": user.username,
                      "role": "Admin" if user == project.admin_user else "Gebruiker",
                      "img": "none"} for user in project.members.all()]

    todos = [
        {
            "name": todo.name,
            "deadline_date": todo.deadline_date,
            "deadline_time": todo.deadline_time,
            "id": todo.id,
            "completed": todo.completed,
            "subtodos": [{"description": subTodo.description, "id": subTodo.id}
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
    selectable_users = {i["username"]: i["id"] for i in
                        get_user_model().objects.filter(
                            is_staff=False).exclude(
                            id=request.user.id).values()}
    temp_users = [user['username'] for user in project_users]
    filtered_selectable_users = {user: id for user, id in
                                 selectable_users.items() if
                                 user not in temp_users}
    selectable_users = json.dumps(filtered_selectable_users)

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
                      "selectable_users": selectable_users,
                  }
                  )


def project_toevoegen_post(request):
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
        add_to_recent(obj, request.user,
                        f"{request.user} heeft project {obj.name} aangemaakt.")
        return HttpResponseRedirect(f"/project/{obj.id}/")

@login_required
def project_toevoegen(request):
    project_toev_form = ProjectForm()
    if request.method == "POST":
       project_toevoegen_post(request)

    selectable_users = {i["username"]: i["id"] for i in
                        get_user_model().objects.filter(
                            is_staff=False).exclude(
                            id=request.user.id).values()}
    selectable_users = json.dumps(selectable_users)

    return render(request, 'project-toevoegen.html',
                  {'title': 'Project toevoegen',
                   'project_form': project_toev_form,
                   "selectable_users": selectable_users})
