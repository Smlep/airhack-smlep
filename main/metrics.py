from .models import *
from .services import distance, SPEED


def compute_distance_stats(tasker):
    tasks = tasker.tasks.all()
    tasks = sorted(tasks, key=lambda t: t.due_time)
    dist = 0
    for i in range(len(tasks) - 1):
        last = tasks[i]
        next = tasks[i + 1]
        dist += distance(last.lat, last.lng, next.lat, next.lng)
    return dist, dist / len(tasks)


class TaskerStats:
    def __init__(self, tasker):
        self.tasker = tasker
        self.mean_distance = None
        self.total_distance = None
        self.total_moving_time = None
        self.mean_moving_time = None

    def compute_personal_metrics(self):
        self.total_distance, self.mean_distance = compute_distance_stats(self.tasker)
        self.total_moving_time = self.total_distance * 60 / SPEED
        self.mean_moving_time = self.mean_distance * 60 / SPEED


def compute_metrics(rq):
    tasks = Task.objects.filter(request=rq)
    taskers = Tasker.objects.filter(request=rq)

    assigned = tasks.exclude(assignee=None)

    task_percentage = len(assigned) / len(tasks)

    print('Percentage ' + str(task_percentage))

    total_distance = 0
    for tasker in taskers:
        total, mean = compute_distance_stats(tasker)
        total_distance += total

    print('Total distance ' + str(total_distance))

    return task_percentage, total_distance


class RequestStats:
    def __init__(self, request):
        self.request = request
        self.task_percentage = None
        self.mean_distance = None
        self.total_distance = None
        self.total_moving_time = None
        self.mean_moving_time = None

    def compute_metrics(self):
        self.task_percentage, self.total_distance = compute_metrics(self.request)
        tasks = Task.objects.filter(request=self.request)
        tasks = tasks.exclude(assignee=None)
        nb_tasks = len(list(tasks))
        self.mean_distance = self.total_distance / nb_tasks
        self.total_moving_time = self.total_distance * 60 / SPEED
        self.mean_moving_time = self.mean_distance * 60 / SPEED
