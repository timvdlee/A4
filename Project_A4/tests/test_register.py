"""
Test geschreven voor register_view door Salah
"""
import pytest
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from mixer.backend.django import mixer
from accounts.views import register_view
from django.test import Client


"""
request factory maakt http-requests voor de test
"""
@pytest.fixture
def factory():
    return RequestFactory()

"""
Maakt user object voor de test
"""
@pytest.fixture
def user():
    return mixer.blend(User)


"""
Maakt eerst http request aan en voegt user eraan toe. 
De test roept dan register_view aan met de HttpRequest en controleert of 
de response statuscode gelijk is aan 302 (de redirect-statuscode) en of de 
response-url gelijk is aan '/' (de homepage).
"""
@pytest.mark.django_db
def test_register_view_authenticated_user(factory, user):
    path = reverse('register')
    request = factory.get(path)
    request.user = user

    response = register_view(request)
    assert response.status_code == 302
    assert response.url == '/'


"""
checkt of de POST-request wordt geaccepteerd en er een redirect plaatsvindt.
"""
@pytest.mark.django_db
def test_register_view_post(factory):
    user = User.objects.create_user(username='testuser', password='testpass')
    client = Client()
    client.login(username='testuser', password='testpass')
    path = reverse('register')
    request = factory.post(path)
    request.user = user
    response = register_view(request)
    assert response.status_code == 302

"""
de HTTP-request (in dit geval de GET-request naar de register_view) succesvol is geweest
en dat er een HTTP-response is teruggegeven die in dit geval een statuscode van 200 heeft.
"""
@pytest.mark.django_db
def test_register_view_unauthenticated_user(factory):
    path = reverse('register')
    request = factory.get(path)
    request.user = AnonymousUser()
    response = register_view(request)
    assert response.status_code == 200

