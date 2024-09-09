from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime
from django.contrib.auth.models import User


# Create your models here.

class Project(models.Model):
    """Project
    Het project model. Hierin staan alle attributen van een project gedefinieerd.
    Een project is het grootste overkoepelende object waarop de hele website draait. 
    
    (Hiërarchie)
    Project - Todo - Subtodo
    
    id = Automatische gegenereerd id voor het project. 
    name = Naam die is meegegeven door de gebruiker. Minimaal 1 character en maximaal 50
    creation_date = De datum waarop het project is gemaakt. Heefet als default de datetime.date.today methode. Hierdoor wordt automatisch vandaag als default creation date genomen. 
    deadline_date = De deadline datum van het project. Heeft als default 1 januari 2024 tenzij de gebruiker iets anders meegeeft
    admin_user = De gebruiker die het project heeft aangemaakt.
    members = Alle leden die lid zijn van dit project

    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    creation_date = models.DateField(default=datetime.date.today)
    deadline_date = models.DateField(default=datetime.date.fromisoformat('2024-01-01'))
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User,
                                     related_name="project_members")

    class Meta:
        db_table = 'Project'
        verbose_name_plural = 'Projecten'


    def __str__(self) -> str:
        return f"Project {self.name} #{self.id}"


class Todo(models.Model):
    """Todo
    De Todo Model. In deze tabel wordt alle informatie over todo's opgeslagen.\
    De todo is het middelste object in de project hiërarchie
    
    Project - Todo - Subtodo
    
    id = Automatisch gegenereerd id.
    project = het project object waarbij de todo hoort.
    name = de gegeven naam aan een todo.
    deadline_date = de deadline datum.
    deadline_time = de deadline tijd.
    completed = of de todo is gemarkeerd als afgerond. 

    """
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
    """SubTodo
    De subtodo is het laatste object in de project hiërarchie
    Project - Todo - Subtodo
    
    id = Automatisch gegenereerd id voor de subtodo
    todo = de todo waarbij de subtodo hoort
    description = de beschrijving van de subtodo

    :param models: _description_
    :return: _description_
    """
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
    """Recent
    
    De recent tabel. Houdt bij wat de recente veranderingen zijn geweest aan elk project
    
    id = Automatisch gegenereerd id
    user = de gebruiker die de aanpassing heeft gedaan
    project = het project waarin de aanpassing is gedaan 
    date = de datum waarop de aanpassing is gedaan
    time = de tijd waarop de aanpassing is gedaan
    description = de beschrijving van wat er is aangepast

    :param models: _description_
    :return: _description_
    """
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
    """Legacy ProfilePicture
    Het model waarin een eventuele profielfoto opgeslagen kan worden.
    Dit was echter gemarkeerd als nice to have en is niet geïmplementeerd

    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    profilepic = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = 'ProfilePicture'
        verbose_name_plural = 'ProfilePictures'

    def __str__(self) -> str:
        return f"Profile picture for {self.user} img: {self.profilepic}"
