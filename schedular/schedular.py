import redis
import time
import json
import sys
import os


from models.db_models import update_task_status,get_pending_tasks
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)


def produce(task):
    try:
        message = {
            "id": task.id,
            "message": task.data["message"],
            "time": task.data["time"],
            "tries": 0
        }
    except KeyError as e:
        print(f"error occured: {e}")
        return
    redis_client.lpush('task_queue', json.dumps(message))
    update_task_status(task.id, "processing")

    print(f"Produced: {message}")


if __name__ == "__main__":
    # produce()

    while True:
        tasks = get_pending_tasks()

        for task in tasks:
            produce(task)
        time.sleep(5)
