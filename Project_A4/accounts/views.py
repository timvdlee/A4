from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm

# Create your views here.

def login_view_POST(request):
    """login_view_POST
    Deze methode geeft alle informatie die de user heeft meegegevn mee aan de django Authentication backend. 
    Django checkt vervolgens of de username & password combinatie correct was. 
    Is dit het geval dan wordt de gebruiker ingelogd. en doorgestuurd naar de homepage. 
    Is dit niet zo dan wordt de gebruiker teruggestuurd naar de login page en wordt er een foutmelding weergegeven. 
    """
    login_form = AuthenticationForm(request, data=request.POST)
    if login_form.is_valid():
        user = login_form.get_user()
        login(request, user)
        return redirect("/")
    else:
        context = {"login_form": login_form,}
        return render(request, "accounts/login.html", context)

def login_view(request):
    """login_view
    
    Deze methode bepaald het gedrag van de login url. 
    Als er een request gestuurd wordt naar de login url kunnen er drie dingen gebeuren 
    Als de gebruiker al ingelogd is dan wordt deze naar de homepage gestuurd. 
    Probeert de gebruiker in te loggen (En is het dus een POST request) dan wordt deze informatie doorgegeven aan de login_view_POST methode
    Zijn beiden niet het geval dan wordt de loginpagina gerendered en aan de gebruiker weergegeven. 

    """
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        return login_view_POST(request)
    else:
        login_form = AuthenticationForm(request, data=request.POST)
        context = {
            "login_form": login_form,
        }
        return render(request, "accounts/login.html", context)
    

def register_view_POST(request):
    """register_view_POST
    Deze view krijgt de request informatie door als de gebruiker een nieuw account probeert aan te maken.
    Deze wordt meegegeven aan de ingebouwde django UserCreationForm. 
    Is deze valid dan wordt de gebruiker opgeslagen in de database en wordt de gebruiker ingelogt. 
    Vervolgens wordt de gebruiker doorgestuurd naar de homepage. 
    
    Voldoet de gebruiker niet aan de eisen. Omdat bijvoorbeeld de twee wachtwoorden niet overeenkomen. 
    Dan wordt de register page opnieuw weergegeven met een passende foutmelding.
    """
    register_form = UserCreationForm(request.POST or None)
    if register_form.is_valid():
        user = register_form.save()
        login(request, user)
        return redirect('/')
    else:
        context = {
            "register_form": register_form,
        }
        return render(request, "accounts/registreer.html", context)

def register_view(request):
    """register
    Deze methode bepaald het gedrag van de register url. 
    Afhankelijk van de inlogstatus en het type request zijn er drie mogelijkheden. 
    Als de user al ingelogt is dan wordt deze doorgestuurd naar de homepage. 
    Probeert de user een nieuw account aan te maken (POST) dan wordt dit doorgestuurd naar de register_view_POST methode
    Anders wordt de ingebouwde django UserCreationForm doorgegeven aan de webpage

    """
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        return register_view_POST(request)
    else:
        register_form = UserCreationForm(request.POST or None)
        context = {
            "register_form": register_form,
        }
        return render(request, "accounts/registreer.html", context)


def logout_view(request):
    """logout
    Deze view logt de gebruiker uit en stuurt de gebruiker vervolgens naar de homepage. 
    Omdat je voor de homepage ingelogt moet zijn wordt je daarna weer naar de loginpagina gestuurd.
    """
    logout(request)
    return redirect("/")


    
