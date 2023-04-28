from .models import Project, User
from django.contrib.auth.decorators import login_required


@login_required
def dropdown_navbar(request):
    projects_with_user = Project.objects.filter(
        members=User.objects.get(id=request.user.id)).order_by('creation_date')
    return {'dropdown_navbar': projects_with_user}
