import redis
import json
import time
import os
import sys
module_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../models"))
sys.path.append(module_path)
from db_models import update_task_status, get_pending_tasks

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


def consume():
    while True:
        _, message = redis_client.brpop('task_queue')
        decoded_message = json.loads(message)
        print("Processing message...")
        try:
            t = decoded_message['time']

            time.sleep(t)
            print(f"task completed {decoded_message['id']}")
            update_task_status(decoded_message['id'], "completed")

        except Exception as e:
            print(f"Json decode error {e}")
            continue

        print(f"Consumed: {message}")


if __name__ == "__main__":
    consume()
