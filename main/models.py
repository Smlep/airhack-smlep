from django.db import models


# Create your models here.


class Request(models.Model):
    batch_id = models.CharField(max_length=50)
    taskers_count = models.IntegerField()
    tasks_count = models.IntegerField()
    time = models.DateTimeField()

    def get_dict(self):
        return {
            "batchId": self.batch_id,
            "taskersCount": self.taskers_count,
            "tasksCount": self.tasks_count,
            "tasks": [task.get_dict() for task in self.tasks.all()]
        }


class Tasker(models.Model):
    tasker_id = models.IntegerField()
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='taskers')


class Task(models.Model):
    task_id = models.CharField(max_length=20)
    due_time = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
    assignee = models.ForeignKey(Tasker, null=True, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='tasks')

    def min_to_str(self, minutes):
        return str(minutes // 60) + ':' + str(minutes % 60)

    def get_dict(self):
        return {
            "dueTime": self.min_to_str(self.due_time),
            "lat": self.lat,
            "lng": self.lng,
            "assignee_id": 1, #self.assignee.id,
            "id": self.task_id
        }
