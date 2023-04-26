from .models import Project, User


def dropdown_navbar(request):
    projects_with_user = Project.objects.filter(
        members=User.objects.get(id=request.user.id)).order_by('creation_date')
    print(projects_with_user)
