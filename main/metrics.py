from .models import *
from .services import distance


def compute_total_distance(tasker):
    tasks = tasker.tasks.all()
    dist = 0
    for i in range(len(tasks) - 1):
        last = tasks[i]
        next = tasks[i + 1]
        dist += distance(last.lat, last.lng, next.lat, next.lng)
    return dist


def compute_metrics(rq):
    tasks = Task.objects.filter(request=rq)
    taskers = Tasker.objects.filter(request=rq)

    assigned = tasks.exclude(assignee=None)

    task_percentage = len(assigned) / len(tasks)

    print('Percentage ' + str(task_percentage))

    total_distance = 0
    for tasker in taskers:
        total_distance += compute_total_distance(tasker)

    print('Total distance ' + str(total_distance))

    return task_percentage, total_distance
