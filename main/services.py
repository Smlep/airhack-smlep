from .models import *

EXECUTION_TIME_TASK = 30
SPEED = 10

def choose_tasks(rq):
    tasks = Task.objects.filter(request=rq)
    taskers = Tasker.objects.filter(request=rq)
    print('Assigning ' + str(len(tasks)) + ' tasks for ' + str(len(taskers)) + ' taskers')
    sorted_tasks = sorted(tasks, key=lambda x: x.due_time)

    for task in sorted_tasks:
        for tasker in taskers:
            if assign_task(tasker, task, EXECUTION_TIME_TASK, SPEED):
                break
