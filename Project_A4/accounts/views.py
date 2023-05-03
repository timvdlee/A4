from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect("/")
        else:
            context = {
                "login_form": login_form,
            }
            return render(request, "accounts/login.html", context)
    else:
        login_form = AuthenticationForm(request, data=request.POST)
        context = {
            "login_form": login_form,
        }
        return render(request, "accounts/login.html", context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
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
    else:
        register_form = UserCreationForm(request.POST or None)
        context = {
            "register_form": register_form,
        }
        return render(request, "accounts/registreer.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")

def get_error_message(form):
    error_msg_str = ""
    for field_name, errors in form.errors.items():
        for error_msg in errors:
            error_msg_str += f"{error_msg}\n"
    return error_msg_str
    
