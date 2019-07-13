from .models import *


def compute_metrics(rq):
    tasks = Task.objects.filter(request=rq)
    taskers = Tasker.objects.filter(request=rq)

    unassigned = tasks.filter(assignee=None)

    task_percentage = 1 - (len(unassigned) / len(taskers))

    print('Percentage ' + str(task_percentage))
