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


def get_curr_pos(tasker, cache=True):
    if cache:
        last_task = tasker.last_task
        if last_task is None:
            return -1, -1
        else:
            return last_task.lat, last_task.lng
    current_tasks = tasker.tasks.all()
    if len(current_tasks) == 0:
        return -1, -1
    sorted_tasks = sorted(current_tasks, key=lambda x: x.due_time)
    return sorted_tasks[-1].lat, sorted_tasks[-1].lng


def cost(tasker, task):
    last_lat, last_lng = get_curr_pos(tasker)
    dist = distance(task.lat, task.lng, last_lat, last_lng)
    moving_time = dist / SPEED

    return moving_time + EXECUTION_TIME_TASK


def set_task(tasker, task):
    task.assignee = tasker
    tasker.last_task = task
    task.save()


def assign_task(tasker, task):
    current_tasks = tasker.tasks.all()
    if len(current_tasks) == 0:
        set_task(tasker, task)
        return True

    sorted_tasks = sorted(current_tasks, key=lambda x: x.due_time)
    last_task = sorted_tasks[-1]
    cost_task = cost(tasker, task)
    if last_task.due_time + cost_task < task.due_time:
        set_task(tasker, task)
        return True

    return False


def get_nearest_unassigned(rq, tasker, travel_time_max=60):
    remaining_tasks = Task.objects.filter(request=rq, assignee=None)
    remaining_tasks = filter(lambda t: tasker.last_task.due_time + cost(tasker, t) < t.due_time, remaining_tasks)
    remaining_tasks = list(filter(lambda t: cost(tasker, t) < travel_time_max, remaining_tasks))

    if len(remaining_tasks) == 0:
        return None

    curr_lat, curr_lng = get_curr_pos(tasker)

    return min(remaining_tasks, key=lambda task: distance(curr_lat, curr_lng, task.lat, task.lng))


def get_earliest_unassigned(rq):
    tasks = Task.objects.filter(request=rq, assignee=None)
    if len(tasks) == 0:
        return None
    sorted_tasks = sorted(tasks, key=lambda x: x.due_time)
    return sorted_tasks[0]


def choose_tasks_chain_access(rq):
    tasks = Task.objects.filter(request=rq)
    taskers = Tasker.objects.filter(request=rq)
    print('Assigning ' + str(len(tasks)) + ' tasks for ' + str(len(taskers)) + ' taskers')
    sorted_tasks = sorted(tasks, key=lambda x: x.due_time)

    for task in sorted_tasks:
        for tasker in taskers:
            if assign_task(tasker, task):
                break


def choose_tasks_closest(rq):
    taskers = Tasker.objects.filter(request=rq)

    for tasker in taskers:
        nearest = get_earliest_unassigned(rq)
        if nearest is None:
            break
        set_task(tasker, nearest)
        nearest = get_nearest_unassigned(rq, tasker)
        while nearest is not None:
            set_task(tasker, nearest)
            nearest = get_nearest_unassigned(rq, tasker)
