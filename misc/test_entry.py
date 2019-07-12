import requests
import json

target_root = 'http://127.0.0.1:8000/'

if __name__ == '__main__':
    url = target_root + 'entry'
    batch_id = 'test'
    taskers_count = 5
    task_count = 50

    obj = {
        'batchId': batch_id,
        'taskersCount': taskers_count,
        'tasksCount': task_count
    }

    content = json.dumps(obj)
    print('Sending:')
    print(content)
    requests.post(url, json=obj)