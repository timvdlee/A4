import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from unittest.mock import patch
from ProjectApp.models import Project
from ProjectApp.views import project_name_edit

@pytest.fixture
def test_user_and_project(db):
    # Create a test user
    test_user = User.objects.create_user(username='testuser', password='testpassword')

    # Create a test project instance
    project = Project.objects.create(name="Old Project Name", admin_user=test_user)

    return test_user, project

def test_project_name_edit_valid_new_name_project_name_changed(test_user_and_project):
    test_user, project = test_user_and_project
    request = HttpRequest()
    request.user = test_user
    request.POST = {'name': 'New Project Name'}

    with patch('ProjectApp.views.add_to_recent') as mock_add_to_recent:
        old_project_name = project.name
        project_name_edit(request, project)
        mock_add_to_recent.assert_called_once_with(
            project, 
            test_user,
            f"{test_user} heeft project {old_project_name} aangepast naar {request.POST.get('name')}"
        )

    project.refresh_from_db()
    assert project.name == 'New Project Name'

def test_project_name_edit_empty_name_no_database_changes(test_user_and_project):
    test_user, project = test_user_and_project
    request = HttpRequest()
    request.user = test_user
    request.POST = {'name': ''}

    project_name_edit(request, project)
    project.refresh_from_db()
    assert project.name == 'Old Project Name'

def test_project_name_edit_name_exceeds_max_length_no_database_changes(test_user_and_project):
    test_user, project = test_user_and_project
    request = HttpRequest()
    request.user = test_user
    request.POST = {'name': 'A' * 51}

    project_name_edit(request, project)
    project.refresh_from_db()
    assert project.name == 'Old Project Name'
