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
    assignee = models.ForeignKey(Tasker, null=True, on_delete=models.CASCADE, related_name='tasks')
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='tasks')

    def min_to_str(self, minutes):
        return "{:02d}".format(minutes // 60) + ':' + "{:02d}".format(minutes % 60)

    def get_dict(self):
        return {
            "dueTime": self.min_to_str(self.due_time),
            "lat": self.lat,
            "lng": self.lng,
            "assignee_id": self.assignee.tasker_id if self.assignee is not None else None,
            "id": int(self.task_id)
        }

    def __str__(self):
        return str(self.get_dict())


def assign_task(tasker, task, EXECUTION_TIME_TASK, SPEED):
    current_tasks = tasker.tasks.all()
    if len(current_tasks) == 0:
        task.assignee = tasker
        task.save()
        return True

    sorted_tasks = sorted(current_tasks, key=lambda x: x.due_time)
    last_task = sorted_tasks[-1]
    if last_task.due_time + EXECUTION_TIME_TASK * 2 < task.due_time:
        task.assignee = tasker
        task.save()
        return True

    return False
