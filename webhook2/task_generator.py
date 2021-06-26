import config
import time
import requests
import json
import uuid
import random
from faker.providers import BaseProvider
from faker import Faker


class TaskProvider(BaseProvider):
    def task_priority(self):
        severity_levels = ['Low', 'Moderate', 'Major', ' Critical']
        return severity_levels[random.randint(0,len(severity_levels)-1)]

fakeTasks = Faker('en_US')
fakeTasks.seed_instance(0)

fakeTasks.add_provider(TaskProvider)

def  make_task(batchid, taskid):
    message = { 'batchid': batchid, 'id':taskid, 'owner':fakeTasks.unique.name(), 'priority': fakeTasks.task_priority()
        }
    return  message

def send_webhook(msg):
    try:
        resp = requests.post(config.WEBHOOK_RECEIVER_URL, data=json.dump(
            msg, sort_keys=True, default=str), headers={'Content-Type':'application/json'}, timeout=1.0)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        pass
    except requests.exceptions.ConnectionError as err:
        pass
    except requests.exceptions.Timeout as err:
        pass
    except requests.exceptions.RequestException as err:
        pass
    except: 
        pass
    else:
         return resp.status_code


def produce_lot_of_tasks():
    n = random.randint(config.MIN_NBR_TASK, config.MAX_NBR_TASK)
    batchid = str(uuid.uuid4())
    for i in range(n):
        msg = make_task(batchid,i)
        resp = send_webhook(msg)
        time.sleep(config.WAIT_TIME)
        print(i, "out of", n, ' --Status', resp, ' --Message = ', msg)
        yield resp, n, msg

if __name__ == "__main__":
    for resp, n, msg in produce_lot_of_tasks():
        pass
