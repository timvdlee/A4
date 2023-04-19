from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here.

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    creation_date = models.DateField()
    deadline_date = models.DateField()
    admin_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    members = models.ManyToManyField(get_user_model())

    class Meta:
        db_table = 'Project'
        verbose_name_plural = 'Projecten'
    def __str__(self) -> str:
        return f"Project {self.name} #{self.id}"


class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    deadline_date = models.DateField()
    deadline_time = models.TimeField()
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'Todo'
        verbose_name_plural = "Todos"
    def __str__(self) -> str:
        return f"Todo {self.id} part of {self.project} name {self.name}"


class SubTodo(models.Model):
    id = models.AutoField(primary_key=True)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'SubTodo'
        verbose_name_plural = "SubTodo's"
    def __str__(self) -> str:
        return f"{self.description} #{self.id} completed {self.completed}"


class Recent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=1024)

    class Meta:
        db_table = 'Recent_edit'
        verbose_name_plural = "Recent_edits"
    def __str__(self) -> str:
        return f"Recent id: {self.id} | {self.date} {self.time} desc {self.description}"


class ProfilePicture(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    profilepic = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = 'ProfilePicture'
        verbose_name_plural = 'ProfilePictures'
    def __str__(self) -> str:
        return f"Profile picture for {self.user} img: {self.profilepic}"
