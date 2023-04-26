"""
URL configuration for Project_A4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ProjectApp.views import (
    home,
    project,
    project_toevoegen
)
from accounts.views import (
    login_view,
    logout_view,
    register_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='homepage'),
    path('project/<int:pk>/', project, name='project'),
    path('project-toevoegen', project_toevoegen, name='project-toevoegen'),
    path("login/", login_view),
    path("registreer/", register_view),
    path("logout/", logout_view),

]
