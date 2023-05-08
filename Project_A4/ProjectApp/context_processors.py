from .models import Project, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def dropdown_navbar(request):
    try:
        projects_with_user = Project.objects.filter(
            members=User.objects.get(id=request.user.id)).order_by('creation_date')
        return {'dropdown_navbar': projects_with_user}

    except ObjectDoesNotExist:
        return ''
