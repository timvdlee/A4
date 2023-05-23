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
    """homepage
    Deze view regelt het gedrag van de homepage. 
    Hij wordt overkoepelt door de @login_required decorator. 
    Wat betekent dat als je niet ingelogt bent dat je naar de login pagina gestuurd zal worden. 
    Deze view bereid veel data voor de de django template later gaat gebruiken. 
    Eerst wroden alle projecten opgehaald waarvan de gebruiker een lid is. Deze worden gesorteerd op de aanmaakdatum. 
    Vervolgens worden alle recente edits opgehaald van de projecten waar de user in zit. 
    Deze worden gestorteerd op datum en tijd. Waarbij de nieuwste bovenaan komt te staan. 
    
    Vervolgens worden deze meegegeven aan de view. Waarbij er bij de recente edits alleen de eerste 10 meegegeven worden.

    """
    projects_with_user = Project.objects.filter(
        members=User.objects.get(id=request.user.id)).order_by('creation_date')
    recent_with_user = Recent.objects.filter(project__in=projects_with_user).order_by('-date', '-time')
    return render(request, 'home.html',
                  {
                      "projects": projects_with_user,
                      "feed": recent_with_user[:10],
                  })

def add_to_recent(project, user, description):
    """add_to_recent
    Deze methode wordt aangeroepen door de POST requests die door de projectpagina gegenereerd worden. 
    Hierin staat een omschrijving van wat er precies is veranderd. 
    De datum en tijd worden hier opgehaald en aan de informatie toegevoegd. 
    Verder wordt de gegeven informatie daarna opgeslagen in de database. 

    :param project: het project waarin de aanpassing is gedaan
    :param user: de gebruiker die de aanpassing heeft gedaan
    :param description: de omschrijving van de aanpassing
    """
    date = datetime.now().date()
    time = datetime.now().time()
    add_recent = Recent(user=user, project=project, date=date, time=time,
                        description=description)
    add_recent.save()
    
def project_name_edit(request,project):
    """project name veranderden 
    Deze methode wordt aangeroepen waarneer de gebruiker een POST request verstuurd vanaf de projectpagina. 
    Specifiek een POST request om de projectnaam te veranderen. 
    Eerst valideert de methode of de nieuwe naam niet te lang is. 
    Is dit het geval dan wordt de naam aangepast en wordt in de Recent edits tabel deze aanpassing gelogt.

    :param request: django request object
    :param project: current project
    """
    new_name = request.POST.get("name")
    if len(new_name) <= Project._meta.get_field('name').max_length:
        add_to_recent(project, request.user, f"{request.user} heeft project {project.name} aangepast naar {request.POST.get('name')}")
        project.name = new_name
        project.save()

def todo_toevoegen_submit(request,project):
    """todo toevoegen aan project
    Deze methode wordt aangeroepen wanneer de gebruiker een nieuwe todo aan wilt maken op de projectpagina
    Specifiek een POST request om de nieuwe todo toe te voegen. 
    Deze informatie wordt verzameld door de TodoForm in forms.py 
    Het enige wat de methode vervolgens doen is het huidige project linken aan de todo.
    Nadat dit is gedaan wordt de todo opgeslagen in de webpagina en wordt deze wijziging gelogt in het recent edits logboek.

    :param request: django request object
    :param project: current project
    """
    todo_form = TodoForm(request.POST)
    todo_form.completed = False
    if todo_form.is_valid():
        td_db_obj = todo_form.save(commit=False)
        td_db_obj.project = project
        td_db_obj.save()
        add_to_recent(project, request.user,
                        f"{request.user} heeft todo {td_db_obj.name} aangemaakt in project {project.name}")
        
def todo_update_submit(request,project):
    """todo in project aanpassen
    Deze methode wordt aangeroepen wanener een gebruiker een todo wilt aanapssen van een project. 
    Dit gebeurd doordat de projectpagina een POST request afstuurd. 
    Eerst wordt de desbetreffende todo opgehaald uit de database waarover het gaat. 
    In deze methode wordt alle informatie opnieuw overschreven. Echter als de user geen aanpassingen doet blijft dit hetzelfde. 
    Verder wordt er nog een validation gedaan om te kijken of de completed checkbox is aangeklikt. Deze wordt gecast naar een boolean. 
    
    Vervoglens word de aanpassing gelogt in het logboek.

    :param request: django request object
    :param project: current project
    """
    todo = Todo.objects.get(id=request.POST.get("id"))
    todo.name = request.POST.get("name")
    todo.project = project
    todo.deadline_date = request.POST.get("deadline_date")
    todo.deadline_time = request.POST.get("deadline_time")
    todo.completed = True if request.POST.get("completed") else False
    todo.save()
    add_to_recent(project, request.user, f"{request.user} heeft todo {todo.name} aangepast")
    
def addSubTodo_submit(request,project):
    """Subtodo toevoegen aan todo
    Deze methode wordt aangeroepen wanneer de gebruiker vanaf de projectpagina een nieuwe subtodo wilt aanmaken. 
    Dit POST request wordt door de projectpagina verstuurd.
    Eerst wordt er gekeken of de lengte van de subtodo boven de 0 is. 
    Is dit het geval dan wordt de SubTodo opgeslagen. Met als todo de overkoepelende todo. 
    Vervolgens wrodt dit opgeslagen in het logboek.

    :param request: django request object
    :param project: current project
    """
    subTodoDesc = request.POST.get("subTodoDesc")
    if len(subTodoDesc) > 0 and len(subTodoDesc) < SubTodo._meta.get_field("description").max_length:
        subtodo = SubTodo()
        subtodo.todo = Todo.objects.get(id=request.POST.get("todoId"))
        subtodo.description = subTodoDesc
        subtodo.save()
        add_to_recent(project, request.user,
                        f"{request.user} heeft een subtodo aangemaakt in todo {subtodo.todo.name} van project {subtodo.todo.project.name}")

def completeSubTodo_submit(request,project):
    """Subtodo afronden in todo
    Deze methode wordt aangeroepen wanneer de gebruiker vanaf de projectpagina een subtodo wilt afronden. 
    Dit gaat doormiddel van een POST request waarin de Id van de subtodo staat. Vervolgens wordt er gekeken naar alle subtodo's met dat id. 
    (Dit is er altijd 1 of 0) Is het er 1 dan wordt dit gelogt en wordt de subtodo verwijdert uit de database. Dit wordt gedaan omdat er op dit moment nog een mogelijkheid is om een subtodo terug te brengen. 
    En om de database schoner te houden wordt de subtodo verwijderd.

    :param request: django request object
    :param project: current project
    """
    subtodo = SubTodo.objects.filter(id=request.POST.get("subTodoId"))
    if len(subtodo) > 0:
        add_to_recent(project, request.user,
                      f"{request.user} heeft een subtodo afgerond van todo {subtodo[0].todo.name} uit project {subtodo[0].todo.project.name}")
        subtodo[0].delete()
        
def reActivateTodo_submit(request,project):
    """Todo opnieuw activeren
    Met deze methode kan een todo die eerder is gemarkeerd als afgerond weer geactiveerd worden. 
    Eerst wordt de desbetreffende todo opgemaakt vervolgens wordt deze weer actief gemaakt. 
    Dit wordt uiteindelijk gelogt in het logboek.

    :param request: django request object
    :param project: current project
    """
    todo = Todo.objects.get(id=request.POST.get("id"))
    todo.completed = False
    todo.save()
    add_to_recent(project, request.user,
                    f"{request.user} heeft todo {todo.name} van project {todo.project.name} opnieuw geactiveerd")
    

def project_add_user(request,project):
    """Gebruiker toevoegen aan project
    Met deze methode kan de gebruiker een nieuwe user toevoegen aan het project. 
    Dit wordt gedaan doormiddel van een POST request vanaf de projectpagina.
    Eerst wordt het desbetreffende project opgehaald waaraan de gebruiker toegevoegt gaat worden. 
    Vervolgens wordt de user opgehaald. Dit wordt gedaan door de username te vergelijken. 
    Vervolgens wordt gekeken of er een resultaat was. Was er geen resultaat dan was de gebruikersnaam niet valid. 
    Is er wel een resultaat en was de gebruikersnaam geldig dan wordt deze gebruiker toegevoegd aan het project en wordt dit gelogt. 

    :param request: django request object
    :param project: current project
    """
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
    """project
    
    Dit is de view die de projectpagina reguleert. 
    Er zijn twee soorten request. POST en GET
    
    Is de request een POST dan zijn er 7 opties mogelijk 
    Deze zijn beschreven in de flowchart. Ook Staan ze aangegeven in de match case expressie. 
    
    Vervolgens als het een GET request is worden eerst alle todo's opgehaald die bij het specifieke project horen. 
    Alleen de todo's die niet gemarkeerd als afgerond zijn worden nu opgehaalt
    Ook worden gelijk alle subtodo's die bij dit project horen ingeladen.
    Vervolgens wordt voor elke todo een apart form aangemaakt voor het geval de gebruiker de todo wilt aanpassen. 
    
    Vervolgens worden alle todo's die gemarkeerd zijn als klaar opgehaalt.
    Daarna wordt het projectform aangemaakt waarmee het project eventueel van naam veranderd kan worden. 
    
    Vervolgens wordt de de form ingeladen waarmee de gebruiker een nieuwe todo kan aanmaken. 
    Verder wordt daarna de form aangemaakt waarmee een nieuwe gebruiker toegevoegdt kan wordne. 
    Hiervoor worden alle mogelijke keuzes meegegeven. Dit zijn alle gebruikers die geen superuser zijn en nog geen lid zijn van het project. 
    Deze worden vervolgens omgezet naar JSON format zodat ze later door de javascript gebruikt kunnen worden.
    

    :param request: _description_
    :param pk: _description_, defaults to None
    :return: _description_
    """
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
    """project toevoegen POST
    De methode die de POST request afhandeld wanneer de gebruiker een POST request wilt maken. 
    Dit wordt voornamelijk afgehandeld door de ProjectForm 
    Echter wordt er apart gekeken naar alle startgebruikers die aan aan een project toegevoegd worden. 
    Hiervan worden de id's opgezocht in de database. 
    Deze gebruikers wroden vervolgens toegevoegd aan de members lijst van het project.
    """
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
    """project toevoegen
    Deze methode wordt beschermt door de @login_required decorator. Waardoor de gebruiker ingelogt moet zijn om deze pagina te kunnen gebruiken.
    Met deze methode wordt er een project toegevoegt. 
    Deze wordt aangeroepen vanaf de project creation pagina. 
    Is het een POST request en dus een verzoek om het project aan te maken dan wordt het request 
    doorgegeven aan de project_toevoegen_post methode. 
    Anders worden eerst alle mogelijke gebruikers meegegeven voor de autocomplete. 
    Alle mogelijke gebruikers zijn alle users die geen superuser zijn. Verder wordt de huidige ingelogde gebruiker ook niet meegenomen. 
    Vervolgens wordt deze informatie verzameld door de ProjectForm uit forms.py
    

    """
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
