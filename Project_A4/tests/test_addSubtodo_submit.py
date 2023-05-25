import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from unittest.mock import patch
from ProjectApp.models import Project, Todo, SubTodo
from ProjectApp.views import addSubTodo_submit, add_to_recent
from datetime import datetime

@pytest.fixture
def test_make_user_project_todo(db):
    test_user = User.objects.create_user(username='testuser', password='testpassword')
    project = Project.objects.create(name="TestProject", admin_user=test_user)
    todo = Todo.objects.create(name="TestTodo",
                               deadline_date=datetime.now().date(),
                               deadline_time=datetime.now().time(),
                               project=project)
    return test_user, project, todo

def test_addSubTodo_submit_creates_subtodo_when_valid_description(test_make_user_project_todo):
    test_user, project, todo = test_make_user_project_todo
    subtodo_len_before = SubTodo.objects.count()
    request = HttpRequest()
    request.user = test_user
    request.POST = {'subTodoDesc': 'Dit is een subtodo',
                    'todoId': project.id}
    addSubTodo_submit(request, project)
    subtodo = SubTodo.objects.filter(todo=todo).last()
    add_to_recent(project,
                  request.user,
                  f"{request.user} heeft een subtodo aangemaakt in todo {subtodo.todo.name} van project {subtodo.todo.project.name}")
    subtodo_len_after = SubTodo.objects.count()
    assert subtodo_len_after == subtodo_len_before + 1


def test_addSubTodo_submit_does_not_create_subtodo_when_empty_description(test_make_user_project_todo):
    test_user, project, todo = test_make_user_project_todo
    request = HttpRequest()
    request.user = test_user
    request.POST = {'subTodoDesc': '',
                    'todoId': project.id}
    subtodo_len_before = SubTodo.objects.count()
    addSubTodo_submit(request, project)
    subtodo_len_after = SubTodo.objects.count()
    assert subtodo_len_after == subtodo_len_before


def test_addSubTodo_submit_does_not_create_subtodo_when_description_exceeds_limit(test_make_user_project_todo):
    test_user, project, todo = test_make_user_project_todo
    request = HttpRequest()
    request.user = test_user
    request.POST = {'subTodoDesc': 'A'*101,
                    'todoId': project.id}
    subtodo_len_before = SubTodo.objects.count()
    addSubTodo_submit(request, project)
    subtodo_len_after = SubTodo.objects.count()
    assert subtodo_len_after == subtodo_len_before
