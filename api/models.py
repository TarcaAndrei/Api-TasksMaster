from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listName = models.CharField(max_length=100)
    def __str__(self):
        return self.listName

class Task(models.Model):
    taskName = models.CharField(max_length=100)
    taskDetails = models.CharField(max_length=300)
    taskDue = models.DateTimeField()
    taskLastUpdated = models.DateTimeField()
    taskPriority = models.CharField(max_length=20)
    taskDone = models.BooleanField()
    taskList = models.ForeignKey(List, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.taskName
    #HOPE ITS working