#!/bin/python3

import datetime
import json
import requests

from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from .models import Request, Tasker, Task
from .services import choose_tasks_chain_access, choose_tasks_closest_one_by_one, choose_tasks_closest_rounds

submission_url = 'http://airhack-api.herokuapp.com/api/submitTasks'
token = 'ilG6KgDxS5EgXzmhLrQuwSl3uQ2VF7pYx2oAVS0Ie9nbwavXo6BAITdFEcwk'
hed = {'Authorization': 'Bearer ' + token}


# Create your views here.

def index(request):
    context = {

    }
    return render(request, 'main/index.html', context)


def minutes_from_string(str):
    nums = str.split(':')
    return int(nums[0]) * 60 + int(nums[1])

def submit(rq):
    dict_res = rq.get_dict()

    print('Sending: ')
    print(json.dumps(dict_res))
    res = requests.post(submission_url, json=dict_res, headers=hed)

    print(res.status_code)
    print(res.text)
    print(res.json())


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

    choose_tasks_closest_rounds(rq)
    print('Saving new request')
    submit(rq)
    return HttpResponse('Received')
