import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from unittest.mock import patch
from ProjectApp.models import Project
from ProjectApp.views import project_toevoegen_post
from django.test import RequestFactory
from django.urls import reverse


@pytest.fixture
def create_test_user(db):
    # Create a test user
    test_user = User.objects.create_user(username='testuser',
                                         password='testpassword')

    # Create a test project instance
    project = Project.objects.create(name="Project Name", admin_user=test_user)

    return test_user, project


@pytest.fixture
def factory():
    return RequestFactory()

@pytest.mark.django_db
def project_toevoegen_post_valid_form_redirect(create_test_user):
    test_user, project = create_test_user
    path = reverse("project-toevoegen")
    request = factory.post(path)
    request.project = project
    response = project_toevoegen_post(request)
    assert response.status_code == 302
