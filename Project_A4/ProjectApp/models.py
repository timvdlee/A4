from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Project(models.Model):
    Naam_project = models.CharField(max_length=100)
    Datum_aangemaakt = models.DateField()
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    #Deadline = models.DateField()
    #Leden = models.CharField()

    class Meta:
        db_table = 'Projecten'


class Todo(models.Model):
    Name_todo = models.CharField(max_length=100)
    Finished = models.BooleanField(default=False)
    Deadline = models.DateField()
    Project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    Gebruiker_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Todos'


class SubTodo(models.Model):
    Name_subtodo = models.CharField(max_length=100)
    Finished = models.BooleanField(default=False)
    Todo_id = models.ForeignKey(Todo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SubTodos'


class Recent(models.Model):
    Gebruiker_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    Date = models.DateField()
    Time = models.TimeField()
    Recent_naam = models.CharField(max_length=100)

    class Meta:
        db_table = 'Recent'


class Gebruiker_extra(models.Model):
    Gebruiker_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Profiel_foto = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = 'Gebruiker_extras'
