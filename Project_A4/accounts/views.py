from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm

# Create your views here.

def login_view_POST(request):
    login_form = AuthenticationForm(request, data=request.POST)
    if login_form.is_valid():
        user = login_form.get_user()
        login(request, user)
        return redirect("/")
    else:
        context = {"login_form": login_form,}
        return render(request, "accounts/login.html", context)

def login_view(request):
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
    logout(request)
    return redirect("/")


    
