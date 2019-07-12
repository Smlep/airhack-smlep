import requests
import json

target_root_local = 'http://127.0.0.1:8000/'
target_root_heroku = 'https://airhack-smlep.herokuapp.com/'

if __name__ == '__main__':
    url = target_root_local + 'entry'
    batch_id = 'test'
    taskers_count = 5
    task_count = 50

    tasks = [{"dueTime": "16:30", "lat": 48.85554319120794, "lng": 2.3613359633447204, "assignee_id": None, "id": 6480}]

    obj = {
        'batchId': batch_id,
        'taskersCount': taskers_count,
        'tasksCount': task_count,
        'tasks': tasks
    }

    print('Sending:')
    print(json.dumps(obj))
    requests.post(url, json=obj)
