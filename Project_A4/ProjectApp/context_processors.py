from .models import Project, User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def dropdown_navbar(request):
    """dropdown_navbar
    
    Deze context_processor wordt in elke view uitgevoerd en maakt een variable globaal beschikbaar. 
    Deze variabele zijn alle projecten waarbij de gebruiker lid van is. Deze wordt weergegeven in de navigatiebar.
    Deze zijn gesorteerd bij de creation date

    :param request: _description_
    :return: _description_
    """
    try:
        projects_with_user = Project.objects.filter(
            members=User.objects.get(id=request.user.id)).order_by('creation_date')
        return {'dropdown_navbar': projects_with_user}

    except ObjectDoesNotExist:
        return ''
