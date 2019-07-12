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

@csrf_exempt
def entry(request):
    json_body = json.loads(request.body)
    batch_id = json_body['batchId']
    taskers_count = json_body['taskersCount']
    task_count = json_body['tasksCount']
    print('batch id: ' + str(batch_id))
    print('taskers count: ' + str(taskers_count))
    now = datetime.datetime.now()
    rq = Request(batch_id=batch_id, taskers_count=taskers_count, tasks_count=task_count, time=now)
    rq.save()
    print('Saving new request')
    return HttpResponse('Received')