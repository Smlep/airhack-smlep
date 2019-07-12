import requests
import json

target_root_local = 'http://127.0.0.1:8000/'
target_root_heroku = 'https://airhack-smlep.herokuapp.com/'

if __name__ == '__main__':
    url = target_root_local + 'entry'
    batch_id = 'test'
    taskers_count = 5
    task_count = 50

    tasks = [{"dueTime": "16:30", "lat": 48.85554319120794, "lng": 2.3613359633447204, "assignee_id": None, "id": 6480},
             {"dueTime": "13:15", "lat": 48.85313729018271, "lng": 2.32256080014798, "assignee_id": None, "id": 9297},
             {"dueTime": "21:45", "lat": 48.838453425693785, "lng": 2.372673134911582, "assignee_id": None, "id": 1889},
             {"dueTime": "11:00", "lat": 48.87672526051465, "lng": 2.314886751843323, "assignee_id": 5,
              "id": 5848414510429},
             {"dueTime": "11:30", "lat": 48.84386891001018, "lng": 2.3611611201332576, "assignee_id": None,
              "id": 92669349229160},
             {"dueTime": "16:30", "lat": 48.85342263737495, "lng": 2.3440113794349227, "assignee_id": None,
              "id": 51259748237216},
             {"dueTime": "18:30", "lat": 48.83955635669002, "lng": 2.3690596145327065, "assignee_id": None,
              "id": 2851363929762},
             {"dueTime": "16:45", "lat": 48.87959373201809, "lng": 2.3581813650566783, "assignee_id": None,
              "id": 14147976438872},
             {"dueTime": "12:15", "lat": 48.84996639880318, "lng": 2.360707548614216, "assignee_id": None,
              "id": 42915031325981},
             {"dueTime": "11:45", "lat": 48.828796160780264, "lng": 2.336318869781783, "assignee_id": None,
              "id": 95088535548880},
             {"dueTime": "12:00", "lat": 48.85655538719948, "lng": 2.3720106986822405, "assignee_id": None,
              "id": 16590672630720},
             {"dueTime": "18:15", "lat": 48.83184083283882, "lng": 2.347887327648211, "assignee_id": None,
              "id": 42068299831144},
             {"dueTime": "17:30", "lat": 48.8565054446245, "lng": 2.3192368943428257, "assignee_id": None,
              "id": 32809195010617},
             {"dueTime": "18:45", "lat": 48.87652462401705, "lng": 2.3371334827783907, "assignee_id": None,
              "id": 70694935298942},
             {"dueTime": "15:30", "lat": 48.87776532349179, "lng": 2.3483439933363917, "assignee_id": None,
              "id": 4293038357046},
             {"dueTime": "12:45", "lat": 48.825332978706484, "lng": 2.350730721762282, "assignee_id": None,
              "id": 27343792983703},
             {"dueTime": "13:15", "lat": 48.84255623613316, "lng": 2.332391072756708, "assignee_id": None,
              "id": 39451799627121}]

    obj = {
        'batchId': batch_id,
        'taskersCount': taskers_count,
        'tasksCount': task_count,
        'tasks': tasks
    }

    print('Sending:')
    print(json.dumps(obj))
    requests.post(url, json=obj)
