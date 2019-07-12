from django.db import models


# Create your models here.


class Request(models.Model):
    batch_id = models.CharField(max_length=50)
    taskers_count = models.IntegerField()
    tasks_count = models.IntegerField()
    time = models.DateTimeField()


class Tasker(models.Model):
    tasker_id = models.IntegerField()
    request = models.ForeignKey(Request, on_delete=models.CASCADE)


class Task(models.Model):
    task_id = models.CharField(max_length=20)
    due_time = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField
    assignee = models.ForeignKey(Tasker, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
