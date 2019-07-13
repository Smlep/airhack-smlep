#!/bin/python3

import datetime
import environ
import json
import requests

from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from .models import Request, Tasker, Task
from .services import choose_tasks_chain_access, choose_tasks_closest_one_by_one, choose_tasks_closest_rounds
from .metrics import compute_metrics, RequestStats, TaskerStats

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    MODE=(str, 'round')
)

environ.Env.read_env('.env')

submission_url = 'http://airhack-api.herokuapp.com/api/submitTasks'
token = 'ilG6KgDxS5EgXzmhLrQuwSl3uQ2VF7pYx2oAVS0Ie9nbwavXo6BAITdFEcwk'
hed = {'Authorization': 'Bearer ' + token}


# Create your views here.

def index(request):
    requests = list(Request.objects.all())
    last_request = requests[-1]
    taskers = Tasker.objects.filter(request=last_request)

    taskers_stats = []

    print(len(taskers))
    for tasker in taskers:
        tstats = TaskerStats(tasker)
        tstats.compute_personal_metrics()
        taskers_stats.append(tstats)

    rstat = RequestStats(last_request)
    rstat.compute_metrics()

    context = {
        'taskers_stats': taskers_stats,
        'request_stats': rstat,
        'extra_name': ': Stats for last request',
        'requests': reversed(requests)
    }
    return render(request, 'main/index.html', context)


def request_details(request, id):
    requests = list(Request.objects.all())
    rq = Request.objects.get(pk=id)

    taskers = Tasker.objects.filter(request=rq)

    taskers_stats = []

    print(len(taskers))
    for tasker in taskers:
        tstats = TaskerStats(tasker)
        tstats.compute_personal_metrics()
        taskers_stats.append(tstats)

    rstat = RequestStats(rq)
    rstat.compute_metrics()

    context = {
        'taskers_stats': taskers_stats,
        'request_stats': rstat,
        'extra_name': ': Stats for ' + rq.batch_id,
        'requests': reversed(requests)
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


@csrf_exempt
def entry(request):
    json_body = json.loads(request.body)
    batch_id = json_body['batchId']
    taskers_count = json_body['taskersCount']
    task_count = json_body['tasksCount']
    now = datetime.datetime.now()
    rq = Request(batch_id=batch_id, taskers_count=taskers_count, tasks_count=task_count, time=now)
    rq.save()

    taskers = [Tasker(tasker_id=i, request=rq) for i in range(1, taskers_count + 1)]
    Tasker.objects.bulk_create(taskers)

    tasks = []
    for task in json_body['tasks']:
        due_time = minutes_from_string(task['dueTime'])
        lat = task['lat']
        lng = task['lng']
        task_id = task['id']
        tasks.append((Task(due_time=due_time, lat=lat, lng=lng, assignee=None, task_id=task_id, request=rq)))

    Task.objects.bulk_create(tasks)
    print('Going for mode ' + str(env('MODE')))
    if env('MODE') == 'round':
        choose_tasks_closest_rounds(rq)
    else:
        choose_tasks_closest_one_by_one(rq)

    print('Saving new request')
    try:
        submit(rq)
    except:
        pass
    compute_metrics(rq)
    return HttpResponse('Received')


def custom_offline(request):
    return render(request, 'main/offline.html', {})


def custom_offline_request(request):
    return render(request, 'main/offline_request.html', {})


def last_cached_request(request):
    return index(request)
