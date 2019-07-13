from .models import *


def compute_metrics(rq):
    tasks = Task.objects.filter(request=rq)

    assigned = tasks.exclude(assignee=None)

    print(len(assigned))
    print(len(tasks))
    task_percentage = len(assigned) / len(tasks)

    print('Percentage ' + str(task_percentage))
