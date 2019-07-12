#!/bin/python3

import datetime
import json

from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from .models import Request, Tasker, Task


# Create your views here.

def index(request):
    context = {

    }
    return render(request, 'main/index.html', context)


def minutes_from_string(str):
    nums = str.split(':')
    return nums[0] * 60 + nums[1]


@csrf_exempt
def entry(request):
    json_body = json.loads(request.body)
    batch_id = json_body['batchId']
    taskers_count = json_body['taskersCount']
    task_count = json_body['tasksCount']
    now = datetime.datetime.now()
    rq = Request(batch_id=batch_id, taskers_count=taskers_count, tasks_count=task_count, time=now)
    rq.save()

    for i in range(1, taskers_count + 1):
        Tasker(tasker_id=i, request=rq).save()

    for task in json_body['tasks']:
        due_time = minutes_from_string(task['dueTime'])
        lat = task['lat']
        lng = task['lng']
        task_id = task['id']
        task = Task(due_time=due_time, lat=lat, lng=lng, assignee=None, task_id=task_id, request=rq)
        task.save()

    print('Saving new request')
    return HttpResponse('Received')
