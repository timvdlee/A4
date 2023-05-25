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

def test_addSubTodo_submit_valid_subtodo_add_to_database(test_make_user_project_todo):
    test_user, project, todo = test_make_user_project_todo
    subtodo_len_before = SubTodo.objects.count()
    request = HttpRequest()
    request.user = test_user
    request.POST = {'subTodoDesc': 'Dit is een subtodo',
                    'todoId': project.id}
    addSubTodo_submit(request, project)
    subtodo = SubTodo.objects.filter(todo=todo).last()
    subtodo_len_after = SubTodo.objects.count()
    assert subtodo_len_after == subtodo_len_before + 1


def test_addSubTodo_submit_empty_subtodo_dont_add_to_database(test_make_user_project_todo):
    test_user, project, todo = test_make_user_project_todo
    request = HttpRequest()
    request.user = test_user
    request.POST = {'subTodoDesc': '',
                    'todoId': project.id}
    subtodo_len_before = SubTodo.objects.count()
    addSubTodo_submit(request, project)
    subtodo_len_after = SubTodo.objects.count()
    assert subtodo_len_after == subtodo_len_before


def test_addSubTodo_submit_to_long_description_dont_add_to_database(test_make_user_project_todo):
    test_user, project, todo = test_make_user_project_todo
    request = HttpRequest()
    request.user = test_user
    request.POST = {'subTodoDesc': 'A'*101,
                    'todoId': project.id}
    subtodo_len_before = SubTodo.objects.count()
    addSubTodo_submit(request, project)
    subtodo_len_after = SubTodo.objects.count()
    assert subtodo_len_after == subtodo_len_before
