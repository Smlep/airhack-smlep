from .models import *
from math import sin, cos, sqrt, atan2, radians

EXECUTION_TIME_TASK = 30  # minutes
SPEED = 10  # km/h


def distance(lat1, lng1, lat2, lng2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lng1 = radians(lng1)
    lng2 = radians(lng2)

    dlon = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def assign_task(tasker, task, EXECUTION_TIME_TASK, SPEED):
    current_tasks = tasker.tasks.all()
    if len(current_tasks) == 0:
        task.assignee = tasker
        task.save()
        return True

    sorted_tasks = sorted(current_tasks, key=lambda x: x.due_time)
    last_task = sorted_tasks[-1]
    dist = distance(task.lat, task.lng, last_task.lat, last_task.lng)
    moving_time = dist / SPEED

    if last_task.due_time + EXECUTION_TIME_TASK  + moving_time < task.due_time:
        task.assignee = tasker
        task.save()
        return True

    return False


def choose_tasks(rq):
    tasks = Task.objects.filter(request=rq)
    taskers = Tasker.objects.filter(request=rq)
    print('Assigning ' + str(len(tasks)) + ' tasks for ' + str(len(taskers)) + ' taskers')
    sorted_tasks = sorted(tasks, key=lambda x: x.due_time)

    for task in sorted_tasks:
        for tasker in taskers:
            if assign_task(tasker, task, EXECUTION_TIME_TASK, SPEED):
                break
