import redis
import json
import time
import os
import sys
import random

module_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../models"))
sys.path.append(module_path)
from db_models import update_task_status, get_pending_tasks

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
MAX_RETRIES = 3 


def consume():
    while True:
        _, message = redis_client.brpop('task_queue')
        decoded_message = json.loads(message)
        print(f"Processing message task : {decoded_message['id']}...")
        tries = decoded_message['tries']
        tries += 1
        decoded_message['tries'] = tries

        try:
            if random.random() < 0.80:
                t = decoded_message['time']
                time.sleep(t)
                print(f"task completed {decoded_message['id']}: {decoded_message['message']}")
                update_task_status(decoded_message['id'], "completed")
            else:
                # simulate execption
                raise Exception("simulated exception")

        except Exception as e:
            print(f"Task failed : {e}")
            if tries < MAX_RETRIES:
                redis_client.lpush("task_queue", json.dumps(decoded_message))
            else:
                redis_client.lpush("dead-letter-queue", json.dumps(decoded_message))

            continue

        # print(f"Consumed: {message}")


if __name__ == "__main__":
    consume()
