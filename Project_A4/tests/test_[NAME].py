# tests/test_project_name_edit.py
import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from unittest.mock import MagicMock,patch
from ProjectApp.models import Project
from ProjectApp.views import project_name_edit

@pytest.mark.django_db
def test_project_name_edit():
    # Create a test user
    test_user = User.objects.create_user(username='testuser', password='testpassword')

    # Mock a project instance
    project = MagicMock(spec=Project)
    project.name = "Old Project Name"
    project._meta.get_field.return_value.max_length = 50

    # Mock a request instance
    request = HttpRequest()
    request.user = test_user
    request.POST = {'name': 'New Project Name'}

    # Mock the add_to_recent function
    with patch('ProjectApp.views.add_to_recent') as mock_add_to_recent:
        project_name_edit(request, project)
        mock_add_to_recent.assert_called_once_with(
            project, 
            test_user,
            f"{test_user} heeft project {project.name} aangepast naar {request.POST.get('name')}"
        )

    # Check if the new name has been saved
    assert project.name == 'New Project Name'
    project.save.assert_called_once()

    # Test case when new name is empty
    request.POST['name'] = ''
    project_name_edit(request, project)
    assert project.name == 'New Project Name'
    project.save.assert_called_once()

    # Test case when new name exceeds max_length
    request.POST['name'] = 'A' * 101
    project_name_edit(request, project)
    assert project.name == 'New Project Name'
    project.save.assert_called_once()
