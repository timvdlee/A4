import pytest
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from mixer.backend.django import mixer
from accounts.views import register_view
from ProjectApp.views import home
from django.test import Client


@pytest.fixture
def factory():
    return RequestFactory()

@pytest.fixture
def user():
    return mixer.blend(User)

@pytest.mark.django_db
def test_register_view_register_autenticated_user_returns_statuscode_url(factory, user):
    path = reverse("register")
    request = factory.get(path)
    request.user = user
    response = register_view(request)
    expect_status_code = 302
    actual_status_code = response.status_code
    assert actual_status_code == expect_status_code
    assert response.url == "/"

@pytest.mark.django_db
def test_register_view_post_login_registered_user_returns_statuscode(factory):
    user = User.objects.create_user(username="testuser", password="testpass")
    client = Client()
    client.login(username="testuser", password="testpass")
    path = reverse("register")
    request = factory.post(path)
    request.user = user
    response = register_view(request)
    expect_status_code = 302
    actual_status_code = response.status_code
    assert actual_status_code == expect_status_code

@pytest.mark.django_db
def test_home_view_unauthenticated_user_redirects_to_login(factory):
    path = reverse("home")
    request = factory.get(path)
    request.user = AnonymousUser()
    response = home(request)
    expect_status_code = 302
    actual_status_code = response.status_code
    assert actual_status_code == expect_status_code
    assert response.url == reverse("login")