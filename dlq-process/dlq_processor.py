import redis 
import json

from models.db_models import update_task_status, get_pending_tasks

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)


def consume():
    while True:
        _, message = redis_client.brpop('dead-letter-queue')
        decoded_message = json.loads(message)
        print(f"failed task {decoded_message['id']}...")

        update_task_status(decoded_message['id'],"failed")

        print(f"updated task: {decoded_message['id']} in db")

        # print(f"Consumed: {message}")


if __name__ == "__main__":
    consume()
