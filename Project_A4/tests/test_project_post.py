import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from unittest.mock import patch
from ProjectApp.models import Project
from ProjectApp.views import project_toevoegen_post
from django.test import RequestFactory
from ProjectApp.forms import ProjectForm
from django.urls import reverse
from datetime import datetime
import json
@pytest.fixture
def create_test_user_and_project(db):
    # Create a test user
    test_user = User.objects.create_user(username='testuser',
                                         password='testpassword')

    # Create a test project instance

    return test_user

@pytest.fixture
def test_make_user_project():
    user1 = User.objects.create_user(username='testuser1', password='testpassword1')
    user2 = User.objects.create_user(username='testuser2', password='testpassword2')
    user3 = User.objects.create_user(username='testuser3', password='testpassword3')
    return [user1, user2, user3]

@pytest.mark.django_db
def test_project_toevoegen_post_valid_project_in_database(create_test_user_and_project, test_make_user_project):
    test_user = create_test_user_and_project
    users = test_make_user_project
    request = HttpRequest()
    request.user = test_user
    request.POST = {'members': json.dumps([user.id for user in users]), "name": "TestProject", "deadline_date": datetime.now().date()}
    request.method = "POST"
    project_toevoegen_post(request)
    assert Project.objects.last().name == "TestProject"

@pytest.mark.django_db
def test_project_toevoegen_post_no_name_project_not_in_database(create_test_user_and_project, test_make_user_project):
    test_user = create_test_user_and_project
    users = test_make_user_project
    request = HttpRequest()
    request.user = test_user
    request.POST = {'members': json.dumps([user.id for user in users]), "name": "", "deadline_date": datetime.now().date()}
    request.method = "POST"
    project_toevoegen_post(request)
    assert Project.objects.count() == 0


@pytest.mark.django_db
def test_project_toevoegen_post_no_deadline_project_not_in_database(create_test_user_and_project, test_make_user_project):
    test_user = create_test_user_and_project
    users = test_make_user_project
    request = HttpRequest()
    request.user = test_user
    request.POST = {'members': json.dumps([user.id for user in users]), "name": "", "deadline_date": ""}
    request.method = "POST"
    project_toevoegen_post(request)
    assert Project.objects.count() == 0
